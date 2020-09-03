# Pull official base image
FROM python:3.8.5
RUN pip install pipenv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER 1

# Set working directory
WORKDIR /dms

# Install dependencies using cache for faster build
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Copy everything else
ADD . .
