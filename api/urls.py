# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    # 博客
    url(r'^blog-list/?$', views.blog_list),
]
