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
