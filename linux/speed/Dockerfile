FROM python:3.6

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends openssh-server sudo systemd rsyslog

RUN useradd -M -s /bin/bash ctf-cracked

RUN useradd -M -s /bin/bash ctf

RUN echo 'ctf:ctf' | chpasswd

RUN usermod -aG sudo ctf

RUN mkdir /challenge

WORKDIR /challenge

COPY challenge/flag.txt .

COPY challenge/read.py .

COPY challenge/sudoers /etc/sudoers

RUN chown root:ctf-cracked flag.txt read.py

RUN chmod 440 flag.txt

RUN chmod 554 read.py

COPY challenge/sshd_config /etc/ssh/sshd_config

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cron psmisc

COPY challenge/crontab /etc/crontab

ENTRYPOINT touch /etc/crontab /etc/cron.*/* \
	    && service cron start \
	    && service rsyslog start \
	    && service ssh start \
	    && tail -f --retry /var/log/auth.log
