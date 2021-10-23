#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

#define UNASSIGNED 0
#define N 9

typedef int Board;

void disable_buffering(void);
int menu(void);
void read_line(char *msg, char *buf, unsigned int max_size);
int read_num(char *msg);
unsigned int random_num(unsigned int min, unsigned int max);
bool find_unassigned(Board board[N][N], int *row, int *col);
bool used_in_row(Board board[N][N], int row, int val);
bool used_in_col(Board board[N][N], int col, int val);
bool used_in_box(Board board[N][N], int box_start_row, int box_start_col, int val);
bool is_safe(Board board[N][N], int row, int col, int val);
void fill_board(Board board[N][N]);
void randomize_board(Board board[N][N]);
void print_board(Board board[N][N]);
bool solve_board(Board board[N][N]);
