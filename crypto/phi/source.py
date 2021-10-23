from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from math import gcd
from secret import flag

def gen_key(bits=2048, e=65537):
    while True:
        p = getPrime(bits)
        q = getPrime(bits)
        phi = (p - 1) * (q - 1)
        if gcd(phi, e) == 1:
            n = p * q
            return n, e, phi

def encrypt(msg, n, e):
    msg_num = bytes_to_long(msg)
    return pow(msg_num, e, n)

def decrypt(cipher, n, d):
    return long_to_bytes(pow(cipher, d, n))

n, e, phi = gen_key()

c = encrypt(flag, n, e)

print(f"n = {n}\nphi = {phi}\nc = {c}")
