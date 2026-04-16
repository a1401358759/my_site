# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    path('blog-list/', views.blog_list),
    path('get-banners/', views.get_banners),
    path('v1/home/', views.home_feed),
    path('v1/archive/', views.archive_timeline),
    path('v1/comments/', views.comments_v1),
    path('v1/articles/<int:article_id>/', views.article_detail),
]
