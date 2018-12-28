FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --user pipenv

COPY . /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN pipenv install

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]