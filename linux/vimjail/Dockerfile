FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y openssh-server vim

COPY challenge /challenge

RUN mv /challenge/vimjail /usr/bin/vimjail && \
    useradd -ms /usr/bin/vimjail prisoner && \
    echo 'prisoner:prisoner' | chpasswd && \
    touch /home/prisoner/.hushlogin

ENTRYPOINT service ssh start && tail -f /dev/null
