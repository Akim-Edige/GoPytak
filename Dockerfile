FROM python:3.11-slim

RUN mkdir code
WORKDIR code

ADD . /code/
ADD .env.docker /code/.env

ENV APP_NAME=DOCKER_APP

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput


CMD daphne -b 0.0.0.0 -p 8000 GoPytak.asgi:application