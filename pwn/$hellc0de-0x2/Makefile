CC=gcc
CFLAGS=-fno-stack-protector -no-pie -z execstack
SOURCE=src/shellcode-2.c
SECCOMP_LIB=seccomp
OUTFILE=challenge/shellcode-2

build: $(SOURCE)
	$(CC) $(CFLAGS) -D BuiltWithMake -o $(OUTFILE) $(SOURCE) -l$(SECCOMP_LIB)
	chmod +x $(OUTFILE)
