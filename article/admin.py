# -*- coding: utf-8 -*-

from django.contrib import admin
from article.models import *
# from django_summernote.admin import SummernoteModelAdmin


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


class OwnerMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')

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


class LinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'weights', 'created_time')
    list_per_page = 10
    ordering = ('-weights',)

    class Media:
        css = {
            'all': ('/static/css/manager.css',)
        }


admin.site.site_title = '博客管理'
admin.site.site_header = '博客后台管理平台'
admin.site.register(Article, ArticleAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(OwnerMessage, OwnerMessageAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Classification)
