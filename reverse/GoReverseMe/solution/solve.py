#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


def fix_b64_padding(s):
    return s + "=" * (4 - len(s) % 4)


def unpad(s):
    return s[: -s[-1]]


key, iv = "SfcpXFw-naJd-7po8lrpwkl-32qTAOqcnuP8tFPZhyQ:D854huw6UpZCzm66-kzddg".split(":")
ct, buff = "RfAh5ZALWb3UmMkHzalgKwOqIL6fAwr_g9PUB5ykZ31V-3btnVEIrYOKgFSb_DIpVawmsZpVWqiE3NZWnvhnewOufL_OAw391Y6ATQ==:D854huw6UpZCzm66-kzddgUz1WV0nDwZ2h0WLZ6l-cAX2u50AW5VqK0f5D6sFcJT".split(":")

key, iv, ct, buff = (
    base64.urlsafe_b64decode(fix_b64_padding(key)),
    base64.urlsafe_b64decode(fix_b64_padding(iv)),
    base64.urlsafe_b64decode(fix_b64_padding(ct)),
    base64.urlsafe_b64decode(fix_b64_padding(buff)),
)

aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
buff = unpad(aes.decrypt(buff[16:]))

flag = bytearray([ct[i] ^ buff[i % len(buff)] for i in range(len(ct))])
print(flag.decode())
