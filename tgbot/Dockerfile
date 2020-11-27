FROM python:3.8.5

RUN pip install pipenv

WORKDIR /tgbot

COPY tgbot/Pipfile* ./

RUN pipenv install

COPY tgbot/ .
