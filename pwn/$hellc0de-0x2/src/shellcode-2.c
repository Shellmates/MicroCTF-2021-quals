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
