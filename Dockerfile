FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED = 1
ENV PYTHONDONTWRITEBYTECODE = 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .