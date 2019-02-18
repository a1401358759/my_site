FROM scratch

LABEL name="registry.cn-beijing.aliyuncs.com/yxf-blog/my_site"
LABEL version="latest"

VOLUME ["/home/data/venv/my_site/my_site", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

RUN mkdir -p /home/data/venv/my_site/my_site/log

ADD entrypoint.sh /home/data/venv/my_site/my_site
RUN chmod +x entrypoint.sh

ADD run.sh /home/data/venv/my_site/my_site
RUN chmod +x run.sh

ADD control.sh /home/data/venv/my_site/my_site
RUN chmod +x control.sh
RUN ln -s control.sh /bin/control

ENTRYPOINT ["entrypoint.sh"]
CMD ["run.sh"]
