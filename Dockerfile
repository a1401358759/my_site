FROM registry.cn-beijing.aliyuncs.com/yxf-blog/my_site

LABEL name="registry.cn-beijing.aliyuncs.com/yxf-blog/my_site"
LABEL version="1508840702"

VOLUME ["/home/data/venv/my_site/my_sitet", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site", "/root/.ssh"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

# create uwsgi pid dir && /opt/django/bin
RUN mkdir -p /var/run/uwsgi
RUN mkdir -p /opt/django/bin
# add entrypoint.sh -- ENTRYPOINT script, setup virtualenv
ADD entrypoint.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/entrypoint.sh
# add run.sh -- CMD script, how to run docker container
ADD run.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/run.sh
# add control.sh -- some container control cmd
ADD control.sh /opt/django/bin/
RUN chmod +x /opt/django/bin/control.sh
RUN ln -s /opt/django/bin/control.sh /bin/control

# Run container
ENTRYPOINT ["/opt/django/bin/entrypoint.sh"]
CMD ["/opt/django/bin/run.sh"]
