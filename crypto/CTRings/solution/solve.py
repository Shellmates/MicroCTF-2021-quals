from challenge import *
from pwn import xor


key = xor(bytes.fromhex(encrypted_msg),msg.encode())

flag = xor(key,bytes.fromhex(encrypted_flag))

print(flag)