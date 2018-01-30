FROM teeks99/clang-ubuntu:3.7
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:ubuntu-toolchain-r/test \

# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
  git \
  wget \
  python \
  python2.7 \
  python2.7-dev \
  python3.4 \
  python3.4-dev \
  libbz2-dev \
  zlib1g-dev \
  libstdc++-6-dev 

# Add the tool configs
ADD user-config.jam /
