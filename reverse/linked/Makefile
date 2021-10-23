CC=gcc
CFLAGS=
SOURCE=src/linked.c
SOURCE_NOFLAG=src/linked-noflag.c
OUTFILE=challenge/linked
OUTFILE_NOFLAG=files/linked

build: $(SOURCE) $(SOURCE_NOFLAG)
	$(CC) $(CFLAGS) -D BuiltWithMake -o $(OUTFILE) $(SOURCE)
	chmod +x $(OUTFILE)
	$(CC) $(CFLAGS) -D BuiltWithMake -o $(OUTFILE_NOFLAG) $(SOURCE_NOFLAG)
	chmod +x $(OUTFILE_NOFLAG)
