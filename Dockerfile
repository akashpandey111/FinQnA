FROM python:3.11.7-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get clean

# install python dependencies
RUN pip install --upgrade pip setuptools
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# add app
COPY . .

RUN curl https://raw.githubusercontent.com/slai-labs/get-beam/main/get-beam.sh -sSfL | sh
RUN beam update
RUN beam configure --clientId=630f03448b8de85f60e2bd0c0838120b --clientSecret=fd3b642a1cfdb6f94d1bb85aaaae7b8a
