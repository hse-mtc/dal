# Python image
FROM python:3.9.1-buster

# Update system and install backup utilities
COPY back-end/docker/image/install-postgres-client.sh /
RUN sh install-postgres-client.sh

# Set working directory
WORKDIR /back-end

# Do not cache bytecode
ENV PYTHONDONTWRITEBYTECODE 1
# Do not buffer stdout & stderr
ENV PYTHONUNBUFFERED 1
# Help Python with imports
ENV PYTHONPATH "src:${PYTHONPATH}"

# Copy Pipfile[.lock]
COPY back-end/Pipfile* ./

# Install pipenv and packages
RUN pip install pipenv && \
    pipenv install --system --deploy --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
