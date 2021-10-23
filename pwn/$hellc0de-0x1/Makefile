CC=gcc
CFLAGS=-fno-stack-protector -no-pie -z execstack
SOURCE=src/shellcode-1.c
OUTFILE=challenge/shellcode-1

build: $(SOURCE)
	$(CC) $(CFLAGS) -D BuiltWithMake -o $(OUTFILE) $(SOURCE)
	chmod +x $(OUTFILE)
