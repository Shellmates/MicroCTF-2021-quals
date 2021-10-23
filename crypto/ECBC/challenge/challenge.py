#!/usr/bin/env python3

from Crypto.Cipher import AES
from secret import FLAG
import os
from binascii import unhexlify

KEY = os.urandom(16)

def welcome():
    print("Welcome into our server !!")
    print("We encrypt the flag using AES-CBC mode, but our decryption service works only with AES-ECB mode")

def decrypt(ciphertext):
    ciphertext = unhexlify(ciphertext)
    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        print({"error": str(e)})
        return ''

    return decrypted.hex()

def encrypt_flag():
    iv = os.urandom(16)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(FLAG)
    ciphertext = iv.hex() + encrypted.hex()

    return ciphertext

def menu():
    print("Here's our menu :\n[1] Encrypt flag\n[2] Decrypt\n[3] Exit\n")
    num = input("Enter a number > ").strip()
    if num == "1":
        print(encrypt_flag() + "\n")
    elif num == "2":
        ciphertext = input("Enter your cipher text > ").strip()
        print(decrypt(ciphertext)+'\n')
    else:
        exit(1)

if __name__ == "__main__":
    welcome()
    while True:
        menu()
