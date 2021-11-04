# Base Python image
FROM python:3.10-buster

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

# Copy pipenv manifests
COPY back-end/Pipfile* ./

# Install pipenv & dependencies
RUN pip install pipenv && \
    pipenv install --system --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
