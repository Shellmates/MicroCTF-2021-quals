#!/usr/bin/python3
import struct

HEAP_DUMP = "23797_mem_55e44a780000-55e44a7813b0.bin"
START_ADDR = 0x55E44A780000
START_OFFSET = 0x4E0
END_OFFSET = 0xB80


class Node:
    def __init__(self, char: int, next_addr: int) -> None:
        self.char = char
        self.next = next_addr


def u64(s: bytes) -> int:
    return struct.unpack("L", s)[0]


with open(HEAP_DUMP, "rb") as f:
    f.seek(START_OFFSET)
    dump = f.read(END_OFFSET - START_OFFSET)

nodes = {}
addresses = []

# each chunk is 32 bytes
# 16 bytes for the Node struct + 16 bytes for heap metadata
for i in range(0, len(dump), 0x20):
    # discard heap metadata
    chunk = dump[i + 0x10 : i + 0x20]

    char = chunk[0]
    next_addr = u64(chunk[8:])
    node_addr = START_ADDR + START_OFFSET + i + 0x10

    nodes[node_addr] = Node(char, next_addr)
    addresses.append(next_addr)

# find the head
for node_addr in nodes:
    if node_addr not in addresses:
        break

flag = []
while node_addr != 0:
    flag.append(nodes[node_addr].char)
    node_addr = nodes[node_addr].next

flag = bytearray(flag).decode()
print(flag)
