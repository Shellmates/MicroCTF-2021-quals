#!/usr/bin/python3

import os

FILE_NAME = "/tmp/A_flag_that_you_can't_catch"
FLAG = "/challenge/flag.txt"

with open(FLAG) as f :
    flag = f.read()

with open(FILE_NAME,"w") as f:
    f.write(flag)

os.remove(FILE_NAME)
