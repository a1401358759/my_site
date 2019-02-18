FROM ubuntu:16.04

VOLUME ["/home/data/venv/my_site/my_site", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

RUN mkdir -p /home/data/venv/my_site/my_site/log
RUN mkdir -p /opt/django/bin

COPY run.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/run.sh

COPY control.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/control.sh

RUN apt-get update && apt-get install -y python-pip

# install "virtualenv", since the vast majority of users of this image will want it
RUN pip install --no-cache-dir virtualenv
RUN ln -s /usr/local/python2.7.11/bin/virtualenv /usr/bin/virtualenv

CMD ["/opt/django/bin/run.sh"]
