from django.contrib import admin
from article.models import *
# Register your models here.
# from django_summernote.admin import SummernoteModelAdmin
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Classification)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content', 'created_at')

    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/config.js',
        )


class OwnerMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')

    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/config.js',
        )


class ArticleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            '/static/tinymce/config.js',
        )
admin.site.register(Article, ArticleAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(OwnerMessage, OwnerMessageAdmin)

