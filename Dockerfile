FROM registry.cn-beijing.aliyuncs.com/yxf-blog/my_site

LABEL name="registry.cn-beijing.aliyuncs.com/yxf-blog/my_site"
LABEL version="latest"

VOLUME ["/home/data/venv/my_site/my_site", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

RUN mkdir -p /home/data/venv/my_site/my_site/log
RUN mkdir -p /opt/django/bin

ADD entrypoint.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/entrypoint.sh

ADD run.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/run.sh

ADD control.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/control.sh

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys C01E1CAD5EA2C4F0B8E3571504C367C218ADD4FF

ENV PYTHON_VERSION 2.7.11

RUN set -x \
    && mkdir -p /usr/src/python \
    && curl -SL "http://sep-protected.oss-cn-beijing.aliyuncs.com/rd/Python-$PYTHON_VERSION.tar.xz" -o python.tar.xz \
    && curl -SL "http://sep-protected.oss-cn-beijing.aliyuncs.com/rd/Python-$PYTHON_VERSION.tar.xz.asc" -o python.tar.xz.asc \
    && gpg --verify python.tar.xz.asc \
    && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
    && rm python.tar.xz* \
    && cd /usr/src/python \
    && ./configure --prefix=/usr/local/python2.7.11 --sysconfdir=/etc/python2.7.11 --libdir=/usr/local/python2.7.11/lib \
    && make -j$(nproc) \
    && make install \
    && ldconfig

RUN mv /usr/bin/python /usr/bin/python2.7.5
RUN ln -s /usr/local/python2.7.11/bin/python /usr/bin/python
RUN sed -i 's/python/python2.7.5/g' /usr/bin/yum
RUN sed -i 's/python/python2.7.5/g' /usr/libexec/urlgrabber-ext-down
RUN curl -SL 'http://sep-protected.oss-cn-beijing.aliyuncs.com/rd/get-pip.py' | python \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && rm -rf /usr/src/python

RUN ln -s /usr/local/python2.7.11/bin/pip /usr/bin/pip
# Add ustc pypi mirror
ADD etc/pip.conf /root/.pip/pip.conf

# install "virtualenv", since the vast majority of users of this image will want it
RUN pip install --no-cache-dir virtualenv
RUN ln -s /usr/local/python2.7.11/bin/virtualenv /usr/bin/virtualenv

ENTRYPOINT ["/opt/django/bin/entrypoint.sh"]
CMD ["/opt/django/bin/run.sh"]
