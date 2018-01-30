FROM teeks99/clang-ubuntu:3.2
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Install pre-reqs
RUN apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
  git \
  wget \
  python2.7 \
  python2.7-dev \
  python3.4 \
  python3.4-dev \
  libbz2-dev \
  zlib1g-dev \
 && cd /usr/bin \
 && ln -s python2.7 python

# Add the tool configs
ADD user-config.jam /
