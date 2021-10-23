#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define MAXLEN 256

typedef struct Node {
  char character;
  struct Node *next;
} Node;

char flag[MAXLEN] = "shellmates{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}";

int main(int argc, char *argv[]) {
  Node *head, *ptr, **dummies;
  int *sequence, temp, idx;
  size_t length;

  srand(time(NULL));

  length = strlen(flag);
  sequence = (int*)calloc(length, sizeof(int));

  for (int i = 0; i < length; i++) {
    sequence[i] = i;
  }

  for (int i = 0; i < length; i++) {
    temp = sequence[i];
    idx = rand() % length;
    sequence[i] = sequence[idx];
    sequence[idx] = temp;
  }

  dummies = (Node**)calloc(length, sizeof(Node*));
  for (int i = 0; i < length; i++) {
    dummies[i] = (Node*)malloc(sizeof(Node));
  }

  head = NULL;

  for (int i = length - 1; i >= 0; i--) {
    free(dummies[sequence[i]]);
    ptr = (Node*)malloc(sizeof(Node));
    ptr->character = flag[i];
    ptr->next = head;
    head = ptr;
  }

  /* Cleanup */

  for (int i = 0; i < length; i++) {
    dummies[i] = NULL;
    sequence[i] = -1;
  }

  /* Stall to dump memory */

  printf("PID: %d\n", getpid());
  getchar();

  return 0;
}
