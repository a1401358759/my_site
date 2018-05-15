# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(verbose_name='\u4f5c\u8005', to='article.Author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(verbose_name='\u5206\u7c7b', to='article.Classification'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=DjangoUeditor.models.UEditorField(null=True, verbose_name='\u6587\u7ae0\u5185\u5bb9', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='count',
            field=models.IntegerField(default=0, verbose_name='\u6587\u7ae0\u70b9\u51fb\u6570'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='article.Tag', verbose_name='\u6807\u7b7e', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='\u90ae\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=30, verbose_name='\u59d3\u540d'),
        ),
        migrations.AlterField(
            model_name='author',
            name='website',
            field=models.URLField(verbose_name='\u4e2a\u4eba\u7f51\u7ad9', blank=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='links',
            name='link',
            field=models.CharField(max_length=100, verbose_name='\u94fe\u63a5\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='links',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u94fe\u63a5\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='links',
            name='weights',
            field=models.SmallIntegerField(default=10, null=True, verbose_name='\u6743\u91cd', blank=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='content',
            field=DjangoUeditor.models.UEditorField(max_length=200, verbose_name='\u7559\u8a00'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u7559\u8a00\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='email',
            field=models.EmailField(max_length=30, verbose_name='\u90ae\u7bb1'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='name',
            field=models.CharField(max_length=30, verbose_name='\u59d3\u540d'),
        ),
        migrations.AlterField(
            model_name='ownermessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='ownermessage',
            name='message',
            field=DjangoUeditor.models.UEditorField(verbose_name='\u5bc4\u8bed'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='creat_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name='\u6807\u7b7e\u540d', blank=True),
        ),
    ]
