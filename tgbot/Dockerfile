# Base Python image
FROM python:3.10-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /tgbot

# Copy pipenv manifests
COPY tgbot/Pipfile* ./

# Install pipenv & packages
RUN pip install pipenv && \
    pipenv install --system --deploy --dev

# Copy everything else
COPY tgbot/ .

# Run bot & server
CMD ["python", "src/bot.py"]
