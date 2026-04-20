FROM teeks99/gcc-ubuntu:6
LABEL org.opencontainers.image.authors="Thomas Kent <docker@teeks99.com>"

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
  python3.8 \
  python3.8-dev \
  libbz2-dev \
  zlib1g-dev

# Add the tool configs
ADD user-config.jam /
