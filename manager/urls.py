# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    # 登入登出
    url(r'^login/?$', views.login_view, name="login_view"),
    url(r'^logout/?$', views.logout_view, name="logout_view"),
    url(r'^change-pw/?$', views.change_passwd_view, name="change_password"),

    # 博客
    url(r'^$', views.blog_list_view, name="blog_list"),
    url(r'^blog-list/?$', views.blog_list_view, name="blog_list"),
    url(r'^blog-create/?$', views.blog_create_view, name="blog_create"),
    url(r'^blog-edit/(?P<item_id>[a-zA-Z0-9]+)/?$', views.blog_edit_view, name="blog_edit"),
    url(r'^blog-del/?$', views.blog_del_view, name="blog_del"),

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

    # 背景音乐
    url(r'^music-list/?$', views.music_list_view, name="music_list"),
    url(r'^music-add/?$', views.add_music_view, name="music_add"),
    url(r'^music-del/?$', views.del_music_view, name="music_del"),

    # 轮播图片
    url(r'^carousel-list/?$', views.carousel_list_view, name="carousel_list"),
    url(r'^carousel-add/?$', views.add_carousel_view, name="carousel_add"),
    url(r'^carousel-del/?$', views.del_carousel_view, name="carousel_del"),

    # 主人寄语
    url(r'^ownmessage-list/?$', views.ownmessage_list_view, name="ownmessage_list"),
    url(r'^ownmessage-add/?$', views.add_ownmessage_view, name="ownmessage_add"),
    url(r'^ownmessage-edit/(?P<item_id>[a-zA-Z0-9]+)/?$', views.edit_ownmessage_view, name="ownmessage_edit"),
    url(r'^ownmessage-del/?$', views.del_ownmessage_view, name="ownmessage_del"),
]
