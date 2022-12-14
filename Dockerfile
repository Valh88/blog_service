FROM python:3.9-alpine3.13
LABEL maintainer="Ivan"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.prod.txt /tmp/requirements.prod.txt
COPY ./app /app
WORKDIR app

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements.prod.txt

#RUN adduser \
#        --disabled-password \
#        --no-create-home \
#        no-sudo-user

#USER no-sudo-user
