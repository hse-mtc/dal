# Python image
FROM python:3.9.1-buster

# Update system and install backup utilities
COPY back-end/docker/image/install-postgres-client.sh /
RUN sh install-postgres-client.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /back-end

# Copy Pipfile[.lock]
COPY back-end/Pipfile* ./

# Install pipenv and packages
RUN pip install pipenv && \
    pipenv install --system --deploy --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
