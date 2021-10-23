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
