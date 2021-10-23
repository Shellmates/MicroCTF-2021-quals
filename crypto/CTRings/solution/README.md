# CTRings

## Write-up

```python
from challenge import *
from pwn import xor


key = xor(bytes.fromhex(encrypted_msg),msg.encode())

flag = xor(key,bytes.fromhex(encrypted_flag))

print(flag)
```

## Flag

`shellmates{CTR_th3_vuln3r4bl3_43S_m0d3}`
