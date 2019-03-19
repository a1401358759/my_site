# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0023_carouselimg_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9c\x80\xe5\x90\x8e\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(max_length=50, verbose_name='\u97f3\u4e50\u540d\u79f0')),
                ('url', models.CharField(max_length=100, verbose_name='\u97f3\u4e50\u5730\u5740')),
                ('cover', models.CharField(max_length=100, verbose_name='\u97f3\u4e50\u5c01\u9762')),
                ('artist', models.CharField(max_length=100, verbose_name='\u827a\u672f\u5bb6')),
                ('lrc', models.CharField(max_length=100, verbose_name='\u97f3\u4e50\u6b4c\u8bcd')),
            ],
            options={
                'verbose_name_plural': '\u80cc\u666f\u97f3\u4e50',
            },
        ),
    ]
