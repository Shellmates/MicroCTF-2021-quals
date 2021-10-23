#!/bin/bash

FLAG_FILE="flag.txt"
TAR_FILE="archive.tar.gz"
NUM=100

# create first gzipped archive or exit if an error occurs
tar czf $TAR_FILE $FLAG_FILE || exit 1

# create nested archives NUM-1 times deep (archive above counts as first one)
# $$ is the process id of current shell/shell script
# $$ is commonly used as a temporary file name
for ((i=0; i < $NUM-1; i++)); do
  tar czf $$ $TAR_FILE
  mv $$ $TAR_FILE
done

# remove flag file
rm $FLAG_FILE
