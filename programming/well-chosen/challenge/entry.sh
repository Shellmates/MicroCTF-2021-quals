#!/bin/bash
socat -dd -T300 tcp-l:7000,reuseaddr,fork,keepalive exec:./server.py
