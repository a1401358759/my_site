# -*- coding: utf-8 -*-

from django.contrib import admin
from article.models import *
# from django_summernote.admin import SummernoteModelAdmin


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content', 'created_at')
    list_per_page = 10
    search_fields = ['name', 'email']
    list_filter = ['created_at', ]

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }

        js = (
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/jquery.form.js',
            '/static/tinymce/config.js',
        )


@admin.register(OwnerMessage)
class OwnerMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'summary', 'created_at')
    list_per_page = 10

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }

        js = (
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/jquery.form.js',
            '/static/tinymce/config.js',
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
            '/static/tinymce/jquery.tinymce.min.js',
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/jquery.form.js',
            '/static/tinymce/config.js',
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
