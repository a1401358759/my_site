# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^blog-list/?$', views.blog_list),
    url(r'^get-banners/?$', views.get_banners),
]
