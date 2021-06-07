# Base Python image
FROM python:3.9.1-buster

# Update system and install backup utilities
COPY back-end/docker/image/install-postgres-client.sh /
RUN sh install-postgres-client.sh

# Install node 14
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt -y install nodejs

# Setup fish
RUN apt -y install fish; chsh -s /usr/bin/fish; mkdir /root/.config; mkdir /root/.config/fish
COPY .devcontainer/config.fish /root/.config/fish

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

# Copy pipenv manifests
COPY back-end/Pipfile* ./

# Install pipenv & dependencies
RUN pip install pipenv && \
    pipenv install --system --dev

# Copy tools
COPY tools /tools

# Copy everything else
COPY back-end .
