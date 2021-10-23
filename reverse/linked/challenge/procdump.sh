#!/bin/sh

[ $# -lt 1 ] && { echo "Usage: $0 PID" >&2; exit 1; }

PID="$1"

cat /proc/$PID/maps | awk '{print $1}' | ( IFS="-"
while read a b; do
    dd if=/proc/$PID/mem bs=$( getconf PAGESIZE ) iflag=skip_bytes,count_bytes \
       skip=$(( 0x$a )) count=$(( 0x$b - 0x$a )) of="${PID}_mem_$a-$b.bin"
done )
