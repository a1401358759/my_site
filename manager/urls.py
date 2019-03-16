# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.blog_list_view, name="blog_list"),
    url(r'^login/?$', views.login_view, name="login_view"),
    url(r'^logout/?$', views.logout_view, name="logout_view"),
    url(r'^blog-list/?$', views.blog_list_view, name="blog_list"),
    url(r'^blog-create/?$', views.blog_create_view, name="blog_create"),

    # 友情链接
    url(r'^friend-links/?$', views.friend_link_list_view, name="friend_link_list"),
    url(r'^friend-add/?$', views.add_friend_link_view, name="friend_link_add"),
    url(r'^friend-del/?$', views.del_friend_link_view, name="friend_link_del"),

    # 文章作者
    url(r'^author-list/?$', views.author_list_view, name="author_list"),
    url(r'^author-add/?$', views.add_author_view, name="author_add"),
    url(r'^author-del/?$', views.del_author_view, name="author_del"),

    # 文章分类
    url(r'^classification-list/?$', views.classification_list_view, name="classification_list"),
    url(r'^classification-add/?$', views.add_classification_view, name="classification_add"),
    url(r'^classification-del/?$', views.del_classification_view, name="classification_del"),

    # 文章标签
    url(r'^tag-list/?$', views.tag_list_view, name="tag_list"),
    url(r'^tag-add/?$', views.add_tag_view, name="tag_add"),
    url(r'^tag-del/?$', views.del_tag_view, name="tag_del"),
]
