import pickle
from binascii import unhexlify
import re
import os
from dotenv import load_dotenv
import io

load_dotenv()

PICKLE_PROTOCOL = 3

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

def serialize(obj):
    p = pickle.dumps(obj, protocol=PICKLE_PROTOCOL)
    serialized = strip_pickle(p)
    return serialized.hex()

def deserialize(hex_serialized):
    serialized = unhexlify(hex_serialized)
    p = pickle.PROTO + bytes([PICKLE_PROTOCOL]) + strip_pickle(serialized) + pickle.STOP
    return restricted_loads(p)
