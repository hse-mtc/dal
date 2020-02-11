# pull official base image
FROM python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
COPY . /code
WORKDIR /code

# install dependencies
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
