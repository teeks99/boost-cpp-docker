FROM teeks99/gcc-ubuntu:4.7
MAINTAINER Thomas Kent <teeks99@yahoo.com>

# Enable future toolchain PPA
RUN apt-get update \
 && apt-get install -y python-software-properties \
 && add-apt-repository -y ppa:git-core/ppa \
 && add-apt-repository -y ppa:ubuntu-toolchain-r/test \

# Install pre-reqs
 && apt-get update \
 && apt-get install -y \
  build-essential \
  git \
  wget \
  python \
  python2.7 \
  python2.7-dev \
  python3.2 \
  python3.2-dev \
  libbz2-dev \
  zlib1g-dev

ADD user-config.jam /
