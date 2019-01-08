FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python3 python-pip && \
    pip install pipenv

COPY . /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN pipenv install

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]