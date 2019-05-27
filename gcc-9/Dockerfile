FROM teeks99/gcc-ubuntu:9
MAINTAINER Thomas Kent <docker@teeks99.com>

# Pre-Req Repos
RUN apt-get update \
 && apt-get install -y software-properties-common \
 && add-apt-repository -y ppa:git-core/ppa \
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
  python-numpy \
  python3.7 \
  python3.7-dev \
  python3-numpy \
  libjpeg-dev \
  libpng-dev \
  libssl-dev \
  libtiff-dev \
  libbz2-dev \
  liblzma-dev \
  libicu-dev \
  libopenmpi-dev \
  zlib1g-dev \
# Speed up fetch
 && git config --global submodule.fetchJobs 40

# Add the tool configs
ADD user-config.jam /

