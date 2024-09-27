# Base Python image
FROM python:3.9.1-bullseye

# Update system and install backup utilities
COPY back-end/docker/image/install-postgres-client.sh /
RUN sh install-postgres-client.sh

# Install node 14
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt -y install nodejs

# Setup starship
RUN curl https://starship.rs/install.sh --output /starship_install.sh; chmod +x /starship_install.sh
RUN sh -c "/starship_install.sh -y"
COPY .devcontainer/starship.toml /root/.config

# Set working directory
WORKDIR /back-end

# Do not cache bytecode
ENV PYTHONDONTWRITEBYTECODE 1
# Do not buffer stdout & stderr
ENV PYTHONUNBUFFERED 1
# Help Python with imports
ENV PYTHONPATH "src:${PYTHONPATH}"

RUN apt-get install ca-certificates curl
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


# Copy pipenv manifests
COPY back-end/Pipfile* ./

# Install pipenv & dependencies
RUN pip install pipenv && \
    pipenv install --system --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
