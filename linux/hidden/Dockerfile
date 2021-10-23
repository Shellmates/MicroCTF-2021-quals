FROM ubuntu:latest

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server systemd rsyslog

RUN useradd -M -s /bin/bash ctf

RUN echo 'ctf:ctf' | chpasswd

RUN mkdir /challenge

WORKDIR /challenge

COPY challenge/flag.txt .flag.txt

ENTRYPOINT service rsyslog start && service ssh start && tail -f --retry /var/log/auth.log
