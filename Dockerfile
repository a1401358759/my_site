FROM ubuntu:16.04
# 声明镜像制作者
MAINTAINER yangxuefeng <13552974161@163.com>
# 设置时区
ENV TZ "Asia/Shanghai"

RUN mkdir -p /home/data/venv/my_site
RUN mkdir -p /home/data/venv/my_site/my_site
RUN mkdir -p /home/data/venv/my_site/log

EXPOSE 8000
WORKDIR /home/data/venv/my_site/my_site

# 安装应用运行所需要的工具依赖pip，git好像没用上，mysql客户端，
RUN apt-get update && apt-get install -y python-pip

RUN pip install --no-cache-dir virtualenv
RUN ln -s /usr/local/python2.7.11/bin/virtualenv /usr/bin/virtualenv

RUN chmod +x run.sh

# 容器启动后要执行的命令
CMD ["run.sh"]
