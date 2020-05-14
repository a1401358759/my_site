> 当前项目所使用环境：Python3.6.8，Django3.0.6

# 项目介绍

##### 1. 后端语言：Python + Django
##### 2. 前端语言：HTML + JQuery + Bootstrap
##### 3. 数据库：MySQL + Redis

# 实现功能

##### 1. 未使用Django-admin，自己手写的管理后台, 用于文章、友链和背景音乐等的在线管理
##### 2. 实现文章按年月、标签和分类归档
##### 3. 实现文章标签云功能
##### 4. 采用第三方评论插件: [Valine](https://valine.js.org/) + [Leancloud](https://leancloud.cn/)
##### 5. 实现文章阅读量统计，12小时内连续访问的IP只记录一次
##### 6. 后台引入wangEditor富文本编辑器和editor.md Markdown编辑器，前端使用prism.js进行代码高亮
##### 7. Celery + Redis + Supervisor进行异步任务和定时任务的启动和进程管理
##### 8. 接入[七牛云存储](https://www.qiniu.com/)，文章中的图片通过接口上传到七牛云
##### 9. 添加过期提醒，文章长时间未更新在详情页设置提醒
##### 10. 友情链接随机排序
##### 11. 支持按文章标题、标签和分类搜索
##### 12. 多数数据存入Redis，提升访问速度

# 项目部署

> 本项目的部署是在Ubuntu18.04的系统上，其他Ubuntu发行版本或者类Unix系统的部署中可能有不同，请知悉。


1. 首先更新系统环境到最新，使其得到更好的兼容

```bash
sudo apt-get update  # 检查是否有可用更新
sudo apt-get upgrade  # 应用更新
sudo apt-get install python3-pip  # 以下为安装相关依赖包
sudo apt-get install locales
sudo apt-get install libmysqlclient-dev
sudo apt-get install python3-mysqldb
sudo apt-get install libssl-dev
sudo apt-get install libcrypto++-dev
sudo apt-get install python3-dev
```

2. 克隆项目

```bash
git clone https://github.com/a1401358759/my_site.git
```

3. 在项目根目录下创建项目所需要的文件夹

```bash
mkdir logs  # 用来存储项目日志
```

4. 新建`local_settings.py`用来覆盖`settings.py`里面的数据库配置

```bash
cp -r my_site/local_settings.py.template local_settings.py
```

5. 进入数据库创建数据库

```bash
CREATE DATABASE `my-site` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

6. 同步数据库

```bash
python3 manage.py migrate
```

7. 安装项目所需要的包

```bash
pip3 install -r requirements.txt
```

8. 因为本项目使用了Redis，所以需要安装redis-server

```bash
sudo apt-get install redis-server  # 安装
redis-server &  # 启动Redis-server
```

9. 运行项目

```bash
python3 manage.py runserver
```

正常情况下，经过以上步骤，就可以通过 `127.0.0.1:8000` 来访问博客首页了，通过  `127.0.0.1:8000/manager` 访问管理端

以上步骤是在本地进行项目测试访问，在线上正式部署还需要安装Nginx、uwsgi、supervisor等。

```bash
sudo apt-get install nginx  # 安装Nginx
sudo pip3 install uwsgi  # 安装uwsgi
sudo apt-get install supervisor  # 安装supervisor
```

1. 复制项目根目录下 `etc/blog.conf` 到 `/etc/nginx/conf.d/` 文件夹下，然后自行修改 `blog.conf` 里面的相关配置

```bash
cp -r etc/blog.conf /etc/nginx/conf.d/blog.conf
```

2. 启动uwsgi

```bash
uwsgi -i etc/uwsgi.ini
```

3. 启动redis-server

```bash
redis-server &  # 此种方法启动redis-server可能有安全隐患，建议使用conf文件启动，具体办法请自行Google
```

4. 使用supervisor启动celery

```bash
supervisord -c etc/supervisor.conf
```

# 注意事项

1. 本文档可能尚有遗漏或者不当之处，如遇问题造成困惑请尽量自行处理或者联系作者，敬请谅解。
2. 本人自己项目目录在 `/home/data/venv/my_site/my_site` 下，如有不同，请自行修改项目代码中出现此地址之处，另：`venv` 是本人统一的项目文件夹，第一个 `my_site` 是项目的virtualenv环境，第二个 `my_site` 是项目根目录。
3. 项目中涉及到的配置文件，如七牛云的 `access_key` 和 `secret_key`，以及leancloud账号的配置，烦请自行注册账号修改，否则侵权必究。

# 捐赠

如果您觉得本项目对您有些许帮助，感谢您的捐赠

![微信](https://img.yangsihan.com/2019_02_11_1709097461.png)![支付宝](https://img.yangsihan.com/2019_02_11_1710581136.png)

# 联系我

1. 邮箱：13552974161@163.com
2. QQ: 1401358759

**本人博客地址:** [我的博客](http://www.yangsihan.com)
