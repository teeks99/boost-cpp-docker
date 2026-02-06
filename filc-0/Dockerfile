FROM teeks99/python2:ubuntu24.04 AS pysrc

FROM cppalliance/droneubuntu2404:filc
LABEL maintainer="Thomas Kent <docker@teeks99.com>"

# Copy in the build of python 2.7
COPY --from=pysrc /usr/local/include/python2.7/ /usr/local/include/python2.7/
COPY --from=pysrc /usr/local/lib/python2.7/ /usr/local/lib/python2.7/
COPY --from=pysrc /usr/local/lib/libpython2.7.so /usr/local/lib/libpython2.7.so.1.0 /usr/local/lib/
COPY --from=pysrc /usr/local/lib/pkgconfig/python-2.7.pc /usr/local/lib/pkgconfig/python.pc /usr/local/lib/pkgconfig/python2.pc /usr/local/lib/pkgconfig/
COPY --from=pysrc /usr/local/bin/python2 /usr/local/bin/python2-config /usr/local/bin/python2.7 /usr/local/bin/smtpd.py /usr/local/bin/python2.7-config /usr/local/bin/2to3 /usr/local/bin/idle /usr/local/bin/pydoc /usr/local/bin/python /usr/local/bin/python-config /usr/local/bin/
RUN ldconfig

# Speed up fetch
RUN echo Staring build \
 # Remove the default 'ubuntu' non-root user, we will create our own at runtime
 && touch /var/mail/ubuntu \
 && chown ubuntu /var/mail/ubuntu \
 && userdel -r ubuntu \
 # Speed up fetch
 &&git config --global submodule.fetchJobs 40

# Add the tool configs
ADD user-config.jam /
