# coding:utf-8

from django.urls import include, re_path
# from django.contrib import admin
from article import views

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    re_path(r'^manager/', include("manager.urls")),
    re_path(r'^api/mysite/', include("api.urls")),
    re_path(r'^$', views.home, name="home"),  # 主页
    re_path(r'^about$', views.about, name="about"),  # 关于我
    re_path(r'^message$', views.message, name="message"),  # 留言
    re_path(r'^links$', views.links, name="links"),  # 友情链接
    re_path(r'^archive/$', views.archive, name="archive"),  # 归档
    re_path(r'^feed/$', views.RSSFeed(), name="RSS"),  # rss订阅
    re_path(r'^search/$', views.blog_search, name="search"),  # 按文章标题搜索
    re_path(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<id>\d+)/$', views.detail, name="detail"),  # 每篇文章
    re_path(r'^article/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archive_month, name="archive_month"),  # 按月归档
    re_path(r'^articleClassfi/(?P<classfi>\w+)/$', views.classfiDetail, name="classfiDetail"),  # 每个分类页下面的文章
    re_path(r'^articleTag/(?P<tag>\w+)/$', views.tagDetail, name="tagDetail"),  # 每个标签页下面的文章
    re_path(r'^love/?$', views.love),
    re_path(r'^my-resume/?$', views.my_resume, name='my_resume'),  # 简历
    re_path(r'^upload/$', views.upload_file, name='upload_file'),
    re_path(r'^upload-rich/$', views.upload_rich_file, name='upload_rich_file'),
    re_path(r'^add-comments/$', views.add_comments_view, name='add_comments'),
    re_path(r'^get-comments/$', views.get_comments_view, name='get_comments'),
]
handler404 = views.page_not_found
