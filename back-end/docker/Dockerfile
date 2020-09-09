# Python 3.8.5 image
FROM python:3.8.5

# Install pipenv
RUN pip install pipenv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /back-end

# Copy Pipfile[.lock]
COPY back-end/Pipfile* ./

# Install packages
RUN pipenv install --system --deploy --dev

# Copy everything else
ADD back-end .

# Copy tools
COPY tools tools
