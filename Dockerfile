FROM registry.cn-beijing.aliyuncs.com/yxf-blog/my_site

LABEL name="registry.cn-beijing.aliyuncs.com/yxf-blog/my_site"
LABEL version="latest"

VOLUME ["/home/data/venv/my_site/my_site", "/home/data/venv/my_site/my_site/log", "/home/data/venv/my_site"]
EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

RUN mkdir -p /home/data/venv/my_site/my_site/log

RUN chmod +x /home/data/venv/my_site/my_site/run.sh
RUN chmod +x /home/data/venv/my_site/my_site/control.sh
RUN chmod +x /home/data/venv/my_site/my_site/entrypoint.sh

ENTRYPOINT ["/home/data/venv/my_site/my_site/entrypoint.sh"]
CMD ["run.sh"]
