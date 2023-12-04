FROM --platform=linux/amd64 python:slim

RUN pip install qbittorrent-api

COPY . .

CMD python -u cleanup.py