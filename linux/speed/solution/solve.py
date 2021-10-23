#!/usr/bin/python3

# Open two ssh sessions 
# First session will run this code that will constantly try to open and read the newly created flag file

while 1:
    try:
        print(open("/tmp/A_flag_that_you_can't_catch").read())
    except:
        pass

# In the second session run constantly sudo -u ctf-cracked /challenge/read.py
