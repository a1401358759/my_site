# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20160520_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85', to='article.Author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', to='article.Classification'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(null=True, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='count',
            field=models.IntegerField(default=0, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x82\xb9\xe5\x87\xbb\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='article.Tag', verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98'),
        ),
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=30, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='author',
            name='website',
            field=models.URLField(verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\xbd\x91\xe7\xab\x99', blank=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='creat_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe5\x90\x8d', blank=True),
        ),
    ]
