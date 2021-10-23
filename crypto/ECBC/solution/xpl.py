#!/usr/bin/python3
from pwn import *
from binascii import hexlify, unhexlify

BLOCK_SIZE = 16
HOST, PORT = "localhost", 7000


def decrypt(block: bytes) -> bytes:
    r.sendline(b"2")
    r.sendlineafter(b"> ", hexlify(block))
    decoded = unhexlify(r.recvline().decode().strip())
    r.recvuntil(b"> ")
    return decoded


r = remote(HOST, PORT)
r.recvuntil(b"> ")

r.sendline(b"1")
flag_enc = unhexlify(r.recvline().decode().strip())
r.recvuntil(b"> ")

flag = b""
for i in range(BLOCK_SIZE, len(flag_enc), BLOCK_SIZE):
    flag += xor(flag_enc[i - BLOCK_SIZE : i], decrypt(flag_enc[i : i + BLOCK_SIZE]))

print(flag.decode())
