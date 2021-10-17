# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    path('blog-list/', views.blog_list),
    path('get-banners/', views.get_banners),
]
