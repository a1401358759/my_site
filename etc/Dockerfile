FROM python:3.9.7-slim

WORKDIR /app

RUN sed -i s@/deb.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list  && \
    sed -i s@/security.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    gcc \
    ssh-client \
    python3-pip \
    python3-mysqldb \
    libssl-dev \
    libcrypto++-dev \
    default-libmysqlclient-dev \
    gnutls-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt --no-cache-dir

COPY . /app/

RUN chmod +x /app/run.sh
# RUN chmod +x /app/etc/control.sh && ln -s /app/etc/control.sh /bin/control

EXPOSE 9000

CMD ["sh", "/app/run.sh"]
