FROM python:3.13
ENV PYTHONUNBUFFERED 1

RUN apt-get clean && apt-get update

RUN mkdir /app
WORKDIR /app

RUN pip install bynder-sdk

COPY . /app/