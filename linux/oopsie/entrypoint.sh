#!/bin/sh

USERSPEC="ctf"
CHROOT_DIR="/chroot"
EXEC="chroot --userspec=${USERSPEC} ${CHROOT_DIR} /shell.sh"
PORT=1337

socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:"$EXEC",stderr
