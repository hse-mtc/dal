# Base Python image
FROM python:3.9.1-buster

# Set working directory
WORKDIR /watchdoc

# Do not cache bytecode
ENV PYTHONDONTWRITEBYTECODE 1
# Do not buffer stdout & stderr
ENV PYTHONUNBUFFERED 1
# Help Python with imports
ENV PYTHONPATH "src:${PYTHONPATH}"

# Copy pipenv manifests
COPY watchdoc/Pipfile* ./

# Install pipenv and packages
RUN pip install pipenv && \
    pipenv install --system --deploy --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY watchdoc .

# Run server
CMD ["python", "src/main.py"]
