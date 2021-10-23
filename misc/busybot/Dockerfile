FROM python:3.8

RUN useradd busybot

COPY app/requirements.txt /tmp/

RUN python -m pip install -r /tmp/requirements.txt

COPY app /app/

WORKDIR /app

RUN chmod +x busybot.py && \
    chmod 111 flag && \
    chown busybot:busybot .env && \
    mv .env /tmp/

USER busybot

ENTRYPOINT ["python", "-u", "./busybot.py"]
