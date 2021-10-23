# speed

## Write-up 

We can run the script `read.py` as `ctf-cracked` using `sudo -u ctf-cracked /challenge/read.py`, which will create a file that we can read but it gets deleted just after the creation.  

So the solution is to open two sessions, in which one of them we run the following python script that keeps trying to read the flag and another session in which we execute the `read.py` as `ctf-cracked`.

### Script

```python
while 1:
    try:
	print(open("/tmp/A_flag_that_you_can't_catch").read())
    except:
	pass
```

## Flag

`shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}`
