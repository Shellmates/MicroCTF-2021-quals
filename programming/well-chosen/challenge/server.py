#!/usr/bin/python3

import random
import time

flag = 'shellmates{I_H0p3_yoU_Wrot3_ThE_5CR1P7}'
lost_mssg = "Your problem solving skills sucks"
error_mssg = "Answer must be numeric"
slow_mssg = "TOOO slow, we said optimized solutions"


def welcome():
	print('''Given an integer array, You need to choose the elements with the maximum sum respecting the next conditions :
- You can start at any position in the array.
- If you take the element at position i you can't take the element at postion i+1
- There are 50 levels and the last one it's a circular list (poistion 0 is connected with poistion n-1)
return the sum of those elements
''')

def print_(mssg):
	print(mssg)
	exit()

def game():
	welcome()
	for i in range(1,51):
		l = generate_list(i*50)
		if i == 50:
			resp = max(solver(l[:-1]),solver(l[1:]))
		else :  
			resp = solver(l)
		l = ','.join(map(str,l))
		print(f'List : {l}')
		start = time.time()
		user_resp = input("Answer : ")
		if not user_resp.isnumeric():
			print_("Answer must be numeric")
		if  resp != int(user_resp) :
			print_(lost_mssg)
		if time.time()-start > 3 :
			print_(slow_mssg)
	print_(flag)

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

def generate_list(count):
	return [random.randint(1,100) for i in range(count)]

if __name__ == '__main__':
	game()
