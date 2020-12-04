FROM python:3.8.5

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /tgbot

COPY tgbot/Pipfile* ./

RUN pipenv install --system --deploy --dev

COPY tgbot/ .
