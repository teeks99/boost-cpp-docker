FROM teeks99/clang-ubuntu:20
LABEL maintainer="Thomas Kent <docker@teeks99.com>"

# Install pre-reqs
RUN apt-get update \
 && apt-get install -y \
  ca-certificates \
  build-essential \
  git \
  wget \
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
  # Python 2.7 Dependencies
  gdb \
  lcov \
  pkg-config \
  libffi-dev \
  libgdbm-dev \
  libgdbm-compat-dev \
  libncurses5-dev \
  libreadline6-dev \
  libsqlite3-dev \
  lzma \
  lzma-dev \
  tk-dev \
  uuid-dev \
# Python 2.7
  && cd /tmp \
  && wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz \
  && tar -xf Python-2.7.18.tgz \
  && cd Python-2.7.18 \
  && ./configure \
  && make -j`nproc` \
  && make install \
# Speed up fetch
 && git config --global submodule.fetchJobs 40

# Add the tool configs
ADD user-config.jam /

