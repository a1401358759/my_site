FROM python:3.9.7-slim

WORKDIR /app

RUN sed -i s@/deb.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list  && \
    sed -i s@/security.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    cron \
    gcc \
    procps \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip3 install -r requirements.txt --no-cache-dir

COPY . /app/

RUN chmod +x /app/run.sh

EXPOSE 8000

CMD ["sh", "/app/run.sh"]
