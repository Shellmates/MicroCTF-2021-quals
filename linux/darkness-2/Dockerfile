FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd ctf

RUN mkdir -p /chroot/usr/bin /chroot/bin /chroot/lib64 /chroot/lib/x86_64-linux-gnu /chroot/dev && \
    mknod /chroot/dev/null c 1 3 && \
    chmod 666 /chroot/dev/null

WORKDIR /lib64

RUN cp ld-linux-x86-64.so.2 /chroot/lib64/

WORKDIR /bin

RUN cp sh cat ls which /chroot/bin/

WORKDIR /usr/bin

RUN cp printf wc tail /chroot/usr/bin/

WORKDIR /lib/x86_64-linux-gnu

RUN cp libc.so.6 libdl.so.2 libpcre.so.3 libpthread.so.0 libselinux.so.1 /chroot/lib/x86_64-linux-gnu/

COPY entrypoint.sh /

COPY flag.txt shell.sh /chroot/

RUN chmod +x /entrypoint.sh /chroot/shell.sh

WORKDIR /chroot

ENTRYPOINT ["/entrypoint.sh"]
