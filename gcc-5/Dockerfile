FROM teeks99/gcc-ubuntu:5
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable PPA
RUN apt-get update \
 && apt-get install -y software-properties-common \

# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  build-essential \
  git \
  wget \
  python \
  python2.7 \
  python2.7-dev \
  python3.4 \
  python3.4-dev \
  libbz2-dev \
  zlib1g-dev

# Add the tool configs
ADD user-config.jam /
