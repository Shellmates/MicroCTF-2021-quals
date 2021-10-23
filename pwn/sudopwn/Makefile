CC=gcc
CFLAGS=
SOURCE=src/sudopwn.c
OUTFILE=challenge/sudopwn

build: $(SOURCE)
	$(CC) $(CFLAGS) -D BuiltWithMake -o $(OUTFILE) $(SOURCE)
	chmod +x $(OUTFILE)
