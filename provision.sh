#!/bin/bash

# Update apt
apt-get update

# Install packages we need:
#
#   - python-setuptools: to easy_install pip
#   - python-dev: development headers so we can compile python C extensions
#   - libpq-dv: PostgreSQL client library headers so we can compile
#       psycopg
#   - libevent-dev: ?
#   - git-core: So we can work with git!
#   - curl: Useful debugging tool
#   - pep8, pyflakes: Useful dev tools for Python
#   - make: Everything needs make.
#   - htop: Useful ops tool.
#   - ruby1.9.3: Ruby 1.9!
apt-get install -y \
  python-setuptools \
  python-dev \
  libpq-dev \
  libevent-dev \
  git-core \
  curl \
  pep8 \
  pyflakes \
  make \
  htop \
  ruby1.9.3

# Install pip because easy_install is just garbage
easy_install pip

## Foreman
gem install foreman --no-ri --no-rdoc

# DONE!
echo "

Provisioning Complete. CTRL+C if this shows for more than a few seconds...

"