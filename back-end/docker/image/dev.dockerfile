# Base Python image
FROM python:3.10-bullseye

# Update system and install backup utilities
COPY back-end/docker/image/install-postgres-client.sh /
RUN sh install-postgres-client.sh

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /back-end

# Do not cache bytecode
ENV PYTHONDONTWRITEBYTECODE 1
# Do not buffer stdout & stderr
ENV PYTHONUNBUFFERED 1
# Help Python with imports
ENV PYTHONPATH "src:${PYTHONPATH}"

# Copy uv manifests
COPY back-end/pyproject.toml back-end/uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
