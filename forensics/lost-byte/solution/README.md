# lost byte

## Write-up

1. File type of broken file :  

```bash
file flag.broken
# flag.broken: data
```

1. Since only the first byte of the file is "lost", we can brute force all possible bytes and generate a new file on each iteration and check whether it has a valid type (i.e: not "data")

2. We can do that with the following [`brute_byte.sh`](./brute_byte.sh) bash script :  

```bash
#!/bin/bash

BROKEN_FILE="flag.broken"
OUTFILE="flag"

# try all bytes 0x00 -> 0xff
for i in {0..255}; do
  byte=$(printf '%x' $i)
  cat <(printf "\x$byte") $BROKEN_FILE >$OUTFILE
  filetype=$(file -b $OUTFILE)
  if [ "$filetype" != "data" ]; then
    echo "(byte 0x$byte) Found possible file type :"
    echo "$OUTFILE: $filetype"
    break
  fi
done
```

3. Let's run the script :  

```bash
./brute_byte.sh
# (byte 0x1f) Found possible file type :
# flag: gzip compressed data, last modified: Tue Jun 22 12:12:21 2021, from Unix
```

It's a `gzip` file.

4. Let's decompress it :  

```bash
gzip -d flag
# gzip: flag: unknown suffix -- ignored
```

`gzip` doesn't like decompressing files without `.gz` extension :)  

5. Rename the file and decompress it :  

```bash
mv flag flag.gz
gzip -d flag.gz
```

6. It decompresses the file to `"flag"`, a TAR archive :  

```bash
file flag
# flag: POSIX tar archive (GNU)
```

7. Un-tar it :  

```bash
tar xvf flag
# flag.txt
```

8. Cat the flag :  

```bash
cat flag.txt
# shellmates{woW_YoU_RECOv3rEd_tHe_fIle!!}
```

## Flag

`shellmates{woW_YoU_RECOv3rEd_tHe_fIle!!}`
