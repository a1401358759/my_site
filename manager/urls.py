# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.blog_list_view, name="blog_list"),
    url(r'^blog-list/?$', views.blog_list_view, name="blog_list"),
]
