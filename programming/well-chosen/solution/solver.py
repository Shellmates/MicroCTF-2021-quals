#!/usr/bin/python3

from pwn import *

def solver(nums):
    n = len(nums)
    if n == 0 : return 0 
    if n == 1 : return nums[0]
    if n == 2 : return max(nums[1],nums[0])
    dp = [0]*n
    dp[0] = nums[0]
    dp[1] = nums[1]
    dp[2] = nums[2]+nums[0]
    i = 3 
    while i < n : 
        dp[i] = nums[i]+max(dp[i-2],dp[i-3])
        i+=1
    return max(dp[n-1],dp[n-2])


IP, PORT = 'localhost', 9000

#r = process('./server.py')
r = remote(IP,PORT)
r.recvuntil('elements\n\n')
for i in range(50):
	r.recvuntil(': ')
	l = list(map(int,r.recvline().strip().split(b',')))
	r.recvuntil(': ')
	if i == 49 : r.sendline(str(max(solver(l[:-1]),solver(l[1:]))))
	else : r.sendline(str(solver(l)))
r.interactive()
