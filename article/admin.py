# -*- coding: utf-8 -*-

from django.contrib import admin
from article.models import *


@admin.register(OwnerMessage)
class OwnerMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'summary', 'created_at')
    list_per_page = 10

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }

        js = (

        )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_time')
    list_per_page = 10
    search_fields = ['title', 'tags__name', 'classification__name']  # 含有外键必须指定外键的字段
    list_filter = ['publish_time', ]
    filter_horizontal = ('tags',)

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }

        js = (

        )


@admin.register(Links)
class LinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'weights', 'created_time')
    list_per_page = 10
    ordering = ('-weights',)

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }


@admin.register(CarouselImg)
class CarouselImgAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'weights', 'created_time')
    list_per_page = 10
    ordering = ('-weights',)

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'url', 'created_time')
    list_per_page = 10
    ordering = ('-created_time',)

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }


admin.site.site_title = '博客管理'
admin.site.site_header = '博客后台管理平台'
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Classification)
