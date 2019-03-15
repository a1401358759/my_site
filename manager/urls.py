# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.blog_list_view, name="blog_list"),
    url(r'^login/?$', views.login_view, name="login_view"),
    url(r'^logout/?$', views.logout_view, name="logout_view"),
    url(r'^blog-list/?$', views.blog_list_view, name="blog_list"),
    url(r'^blog-create/?$', views.blog_create_view, name="blog_create"),
]
