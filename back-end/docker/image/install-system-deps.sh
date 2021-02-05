#!/usr/bin/env sh

set -e -x

# Update system
apt-get update

# Install tool for automatic system release identification
apt-get install -y lsb-release

# Let `apt` know about Postgres repositories
# Taken from here: https://wiki.postgresql.org/wiki/Apt
apt-get install -y curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Update system again
apt-get update

# Install Postgres client (its version should preferably match service image)
apt-get install -y postgresql-client-13

# Install cron
apt-get -y install cron
