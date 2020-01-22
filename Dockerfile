# pull official base image
FROM python:3.7

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/