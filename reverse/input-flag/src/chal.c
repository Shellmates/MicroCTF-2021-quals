#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
  char input[256];

  printf("Input flag : ");
  fgets(input, 256, stdin);

  if (!strcmp(input, "shellmates{l3t$_St4Rt_R3vErS1Ng_FOR_RE4L_NoW}")) {
    printf("Correct flag !\n");
  } else {
    printf("Wrong flag !\n");
  }

  return 0;
}
