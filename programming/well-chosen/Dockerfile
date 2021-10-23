FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y  python3 socat
RUN useradd -m -d /home/ouxzama -s /bin/bash ouxzama

WORKDIR /home/ouxzama
COPY challenge/entry.sh /home/ouxzama/entry.sh
COPY challenge/server.py /home/ouxzama/server.py
RUN chmod 555 entry.sh
RUN chmod 555 server.py

EXPOSE 7000

USER ouxzama

ENTRYPOINT /home/ouxzama/entry.sh