import pickle
import hashlib
from binascii import unhexlify
import re
import os
from dotenv import load_dotenv
import io

load_dotenv()

HASHFUNC = "md5"
PICKLE_PROTOCOL = 3
KEY = os.getenv("KEY").encode()
# len(KEY) == 12

class InvalidSignature(Exception):
    pass

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        raise pickle.UnpicklingError("Trust me, you don't need that")

def restricted_loads(s):
    return RestrictedUnpickler(io.BytesIO(s)).load()

def strip_pickle(p):
    # skip protocol
    s = re.sub(b'\x80.', b'', p)
    # skip stop instruction
    return re.sub(b'\\.', b'', s)

def serialize(obj, hashfunc=HASHFUNC):
    p = pickle.dumps(obj, protocol=PICKLE_PROTOCOL)
    serialized = strip_pickle(p)
    h = hashlib.new(hashfunc, KEY + serialized)
    signature = h.hexdigest()
    return signature, serialized.hex()

def deserialize(signature, hex_serialized, hashfunc=HASHFUNC):
    serialized = unhexlify(hex_serialized)
    h = hashlib.new(hashfunc, KEY + serialized)
    computed = h.hexdigest()
    if computed != signature:
        raise InvalidSignature("Signatures don't match")
    p = pickle.PROTO + bytes([PICKLE_PROTOCOL]) + strip_pickle(serialized) + pickle.STOP
    return restricted_loads(p)
