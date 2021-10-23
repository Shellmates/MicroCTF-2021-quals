#!/usr/bin/env python3

import pickle
from binascii import unhexlify
from sys import argv, stderr, exit

payload = pickle.dumps([1337, 1337.0, '1337', b'1337'])

if __name__ == "__main__":
    print(f"[+] Serialized hex data : {payload.hex()}")
