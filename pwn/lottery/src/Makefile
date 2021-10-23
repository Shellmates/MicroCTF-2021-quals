CC=gcc
CFLAGS=-no-pie -fstack-protector
SOURCE=lottery.c
OUTFILE=../challenge/lottery

all: $(SOURCE)
	$(CC) $(SOURCE) $(CFLAGS) -o $(OUTFILE)
clean: $(OUTFILE)
	rm -f $(OUTFILE)
