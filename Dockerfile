FROM registry.cn-beijing.aliyuncs.com/yxf-blog/my_site

LABEL name="registry.cn-beijing.aliyuncs.com/yxf-blog/my_site"
LABEL version="latest"

VOLUME ["/home/data/venv/my_site/my_site", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

RUN mkdir -p /home/data/venv/my_site/my_site/log

ADD /home/data/venv/my_site/my_site/run.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/run.sh


ADD /home/data/venv/my_site/my_site/control.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/control.sh
RUN ln -s /opt/django/bin/control.sh /bin/control

RUN mkdir -p /opt/django/bin
ADD /home/data/venv/my_site/my_site/entrypoint.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/entrypoint.sh

ENTRYPOINT ["/opt/django/bin/entrypoint.sh"]
CMD ["/opt/django/bin/run.sh"]
