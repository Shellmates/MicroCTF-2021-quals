# ECBC

## Write-up

The network service does two simple operations:
1. Encrypt the flag using AES in CBC mode.
2. Decrypt anything we give it using AES in ECB mode.

Let's first recall how AES encryption works in CBC mode:
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/Cbc_encryption.png" alt="AES-CBC decryption" />
</p>

and how AES decryption works in ECB mode:
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/6/66/Ecb_decryption.png" alt="AES-CBC decryption" />
</p>

We basically have a way to decrypt individual blocks using AES, after that, we just perform the `XOR`ing manually with the previous block of ciphertext to recover the flag.

```python
#!/usr/bin/python3
from pwn import *
from binascii import hexlify, unhexlify

BLOCK_SIZE = 16
HOST, PORT = "localhost", 7000


def decrypt(block: bytes) -> bytes:
    r.sendline(b"2")
    r.sendlineafter(b"> ", hexlify(block))
    decoded = unhexlify(r.recvline().decode().strip())
    r.recvuntil(b"> ")
    return decoded


r = remote(HOST, PORT)
r.recvuntil(b"> ")

r.sendline(b"1")
flag_enc = unhexlify(r.recvline().decode().strip())
r.recvuntil(b"> ")

flag = b""
for i in range(BLOCK_SIZE, len(flag_enc), BLOCK_SIZE):
    flag += xor(flag_enc[i - BLOCK_SIZE : i], decrypt(flag_enc[i : i + BLOCK_SIZE]))

print(flag.decode())
```

## Flag

`shellmates{_d0n7_C0mb1n3_M0de5_}`
