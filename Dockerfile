FROM --platform=linux/arm64 python:slim

RUN pip install qbittorrent-api

COPY . .

CMD python -u cleanup.py