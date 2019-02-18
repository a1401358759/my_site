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
RUN ln -s /opt/django/bin/control.sh /bin/control

ENTRYPOINT ["/opt/django/bin/entrypoint.sh"]
CMD ["/opt/django/bin/run.sh"]
