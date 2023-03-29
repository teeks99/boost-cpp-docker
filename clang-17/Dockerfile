FROM teeks99/clang-ubuntu:17
LABEL maintainer="Thomas Kent <docker@teeks99.com>"

# Install pre-reqs
RUN apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
  git \
  wget \
  python2.7 \
  python2.7-dev \
  python3 \
  python3-dev \
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

