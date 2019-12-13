# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views


urlpatterns = [
    # 登入登出
    re_path(r'^login/?$', views.login_view, name="login_view"),
    re_path(r'^logout/?$', views.logout_view, name="logout_view"),
    re_path(r'^change-pw/?$', views.change_passwd_view, name="change_password"),

    # 博客
    re_path(r'^$', views.blog_list_view, name="blog_list"),
    re_path(r'^blog-list/?$', views.blog_list_view, name="blog_list"),
    re_path(r'^blog-create/?$', views.blog_create_view, name="blog_create"),
    re_path(r'^blog-edit/(?P<item_id>[a-zA-Z0-9]+)/?$', views.blog_edit_view, name="blog_edit"),
    re_path(r'^blog-del/?$', views.blog_del_view, name="blog_del"),
    re_path(r'^blog-update-status/?$', views.blog_update_status_view, name="blog_update_status"),

    # 友情链接
    re_path(r'^friend-links/?$', views.friend_link_list_view, name="friend_link_list"),
    re_path(r'^friend-add/?$', views.add_friend_link_view, name="friend_link_add"),
    re_path(r'^friend-del/?$', views.del_friend_link_view, name="friend_link_del"),

    # 文章作者
    re_path(r'^author-list/?$', views.author_list_view, name="author_list"),
    re_path(r'^author-add/?$', views.add_author_view, name="author_add"),
    re_path(r'^author-del/?$', views.del_author_view, name="author_del"),

    # 文章分类
    re_path(r'^classification-list/?$', views.classification_list_view, name="classification_list"),
    re_path(r'^classification-add/?$', views.add_classification_view, name="classification_add"),
    re_path(r'^classification-del/?$', views.del_classification_view, name="classification_del"),

    # 文章标签
    re_path(r'^tag-list/?$', views.tag_list_view, name="tag_list"),
    re_path(r'^tag-add/?$', views.add_tag_view, name="tag_add"),
    re_path(r'^tag-del/?$', views.del_tag_view, name="tag_del"),

    # 背景音乐
    re_path(r'^music-list/?$', views.music_list_view, name="music_list"),
    re_path(r'^music-add/?$', views.add_music_view, name="music_add"),
    re_path(r'^music-del/?$', views.del_music_view, name="music_del"),

    # 轮播图片
    re_path(r'^carousel-list/?$', views.carousel_list_view, name="carousel_list"),
    re_path(r'^carousel-add/?$', views.add_carousel_view, name="carousel_add"),
    re_path(r'^carousel-del/?$', views.del_carousel_view, name="carousel_del"),

    # 主人寄语
    re_path(r'^ownmessage-list/?$', views.ownmessage_list_view, name="ownmessage_list"),
    re_path(r'^ownmessage-add/?$', views.add_ownmessage_view, name="ownmessage_add"),
    re_path(r'^ownmessage-edit/(?P<item_id>[a-zA-Z0-9]+)/?$', views.edit_ownmessage_view, name="ownmessage_edit"),
    re_path(r'^ownmessage-del/?$', views.del_ownmessage_view, name="ownmessage_del"),

    # 清除缓存
    re_path(r'^clear-caches/?$', views.clear_caches_view, name="clear_caches")
]
