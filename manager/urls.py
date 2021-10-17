# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    # 登入登出
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('change-pw/', views.change_passwd_view, name="change_password"),

    # 博客
    path('', views.blog_list_view, name="blog_list"),
    path('blog-list/', views.blog_list_view, name="blog_list"),
    path('blog-create/', views.blog_create_view, name="blog_create"),
    path('blog-edit/<int:item_id>/', views.blog_edit_view, name="blog_edit"),
    path('blog-del/', views.blog_del_view, name="blog_del"),
    path('blog-update-status/', views.blog_update_status_view, name="blog_update_status"),

    # 友情链接
    path('friend-links/', views.friend_link_list_view, name="friend_link_list"),
    path('friend-add/', views.add_friend_link_view, name="friend_link_add"),
    path('friend-del/', views.del_friend_link_view, name="friend_link_del"),

    # 文章作者
    path('author-list/', views.author_list_view, name="author_list"),
    path('author-add/', views.add_author_view, name="author_add"),
    path('author-del/', views.del_author_view, name="author_del"),

    # 文章分类
    path('classification-list/', views.classification_list_view, name="classification_list"),
    path('classification-add/', views.add_classification_view, name="classification_add"),
    path('classification-del/', views.del_classification_view, name="classification_del"),

    # 文章标签
    path('tag-list/', views.tag_list_view, name="tag_list"),
    path('tag-add/', views.add_tag_view, name="tag_add"),
    path('tag-del/', views.del_tag_view, name="tag_del"),

    # 背景音乐
    path('music-list/', views.music_list_view, name="music_list"),
    path('music-add/', views.add_music_view, name="music_add"),
    path('music-del/', views.del_music_view, name="music_del"),

    # 轮播图片
    path('carousel-list/', views.carousel_list_view, name="carousel_list"),
    path('carousel-add/', views.add_carousel_view, name="carousel_add"),
    path('carousel-del/', views.del_carousel_view, name="carousel_del"),

    # 主人寄语
    path('ownmessage-list/', views.ownmessage_list_view, name="ownmessage_list"),
    path('ownmessage-add/', views.add_ownmessage_view, name="ownmessage_add"),
    path('ownmessage-edit/<int:item_id>/', views.edit_ownmessage_view, name="ownmessage_edit"),
    path('ownmessage-del/', views.del_ownmessage_view, name="ownmessage_del"),

    # 清除缓存
    path('clear-caches/', views.clear_caches_view, name="clear_caches")
]
