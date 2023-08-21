FROM python:3.11-alpine

ENV PYTHONUNBUFFERED = 1
ENV PYTHONDONTWRITEBYTECODE = 1

WORKDIR /app

RUN apk update
RUN apk add geos-dev geos make automake gcc g++ subversion python3-dev

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .