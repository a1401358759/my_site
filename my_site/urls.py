# coding:utf-8

from django.conf.urls import include, url
# from django.contrib import admin
from article import views

urlpatterns = [
    # url(r'^manager/', include(admin.site.urls)),
    url(r'^manager/', include("manager.urls")),
    url(r'^api/mysite/', include("api.urls")),
    url(r'^$', views.home, name="home"),  # 主页
    url(r'^about$', views.about, name="about"),  # 关于我
    url(r'^message$', views.message, name="message"),  # 留言
    url(r'^links$', views.links, name="links"),  # 友情链接
    url(r'^archive/$', views.archive, name="archive"),  # 归档
    url(r'^feed/$', views.RSSFeed(), name="RSS"),  # 新添加的urlconf, 并将name设置为RSS, 方便在模板中使用
    url(r'^search/$', views.blog_search, name="search"),  # 按文章标题搜索
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<id>\d+)/$', views.detail, name="detail"),  # 每篇文章
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archive_month, name="archive_month"),  # 按月归档
    url(r'^articleClassfi/(?P<classfi>\w+)/$', views.classfiDetail, name="classfiDetail"),  # 每个分类页下面的文章
    url(r'^articleTag/(?P<tag>\w+)/$', views.tagDetail, name="tagDetail"),  # 每个标签页下面的文章
    url(r'^love/?$', views.love),
    url(r'^my-resume/?$', views.my_resume, name='my_resume'),  # 简历
    url(r'^upload/$', views.upload_file, name='upload_file'),
    url(r'^upload-rich/$', views.upload_rich_file, name='upload_rich_file'),
]
