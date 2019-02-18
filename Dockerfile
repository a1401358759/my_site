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
RUN apt-get -y install epel-release && \
    apt-get -y install python-pip && \
    apt-get -y install git nginx gcc gcc-c++ python-devel && apt-get -y install mysql && \
    apt-get -y install mysql-devel && apt-get clean all && \
    pip install --upgrade pip

RUN pip install --no-cache-dir virtualenv
RUN ln -s /usr/local/python2.7.11/bin/virtualenv /usr/bin/virtualenv

RUN chmod u+x run.sh
# 容器启动后要执行的命令
CMD ["run.sh"]
