FROM teeks99/python2:ubuntu24.04 AS pysrc

FROM teeks99/clang-ubuntu:23
LABEL maintainer="Thomas Kent <docker@teeks99.com>"

# Copy in the build of python 2.7
COPY --from=pysrc /usr/local/include/python2.7/ /usr/local/include/python2.7/
COPY --from=pysrc /usr/local/lib/python2.7/ /usr/local/lib/python2.7/
COPY --from=pysrc /usr/local/lib/libpython2.7.so /usr/local/lib/libpython2.7.so.1.0 /usr/local/lib/
COPY --from=pysrc /usr/local/lib/pkgconfig/python-2.7.pc /usr/local/lib/pkgconfig/python.pc /usr/local/lib/pkgconfig/python2.pc /usr/local/lib/pkgconfig/
COPY --from=pysrc /usr/local/bin/python2 /usr/local/bin/python2-config /usr/local/bin/python2.7 /usr/local/bin/smtpd.py /usr/local/bin/python2.7-config /usr/local/bin/2to3 /usr/local/bin/idle /usr/local/bin/pydoc /usr/local/bin/python /usr/local/bin/python-config /usr/local/bin/

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
# Speed up fetch
 && git config --global submodule.fetchJobs 40 \
 # Find Python 2 shared objects
 && ldconfig

# Add the tool configs
ADD user-config.jam /

