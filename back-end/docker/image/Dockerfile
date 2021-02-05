# Python image
FROM python:3.9.1-buster

# Update system and install system-wide dependencies
COPY back-end/docker/image/install-system-deps.sh /
RUN sh install-system-deps.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /back-end

# Copy Pipfile[.lock]
COPY back-end/Pipfile* ./

# Install `pipenv` and packages
RUN pip install pipenv && \
    pipenv install --deploy --dev

# Copy tools
COPY tools /tools

# Copy crontab with periodic tasks
COPY back-end/cron/tasks /etc/cron.d/tasks

# Make sure permissions are right
RUN chmod -R 0644 /etc/cron.d/

# Let `cron` know about tasks
RUN crontab /etc/cron.d/tasks

# Copy everything else
COPY back-end .
