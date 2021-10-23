# serializer

## Write-up

- The application allows serializing any string and deserializing any (allowed) pickle object

- The goal is to make the application deserialize to the following to get the flag :

```python
  if data == [1337, 1337.0, '1337', b'1337']:
      return render_template("index.html", flag=FLAG)
```

- Let's try to craft the serialized payload :

```python
import pickle
from binascii import unhexlify
from sys import argv, stderr, exit

payload = pickle.dumps([1337, 1337.0, '1337', b'1337'])

if __name__ == "__main__":
    print(f"[+] Serialized hex data : {payload.hex()}")
```

- Payload : `80035d7100284d3905474094e4000000000058040000003133333771014304313333377102652e`

- Passing this payload to the deserializer, we get the flag : `shellmates{Check_OUt_My_SeCUr3_S3RiAlIZ3R_nEXt}`

## Flag

`shellmates{Check_OUt_My_SeCUr3_S3RiAlIZ3R_nEXt}`
