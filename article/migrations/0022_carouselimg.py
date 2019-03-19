# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0021_ownermessage_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9c\x80\xe5\x90\x8e\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(max_length=50, verbose_name='\u56fe\u7247\u540d\u79f0')),
                ('description', models.CharField(max_length=100, verbose_name='\u56fe\u7247\u63cf\u8ff0')),
                ('path', models.CharField(max_length=100, verbose_name='\u56fe\u7247\u5730\u5740')),
                ('weights', models.SmallIntegerField(default=10, null=True, verbose_name='\u56fe\u7247\u6743\u91cd', blank=True)),
            ],
            options={
                'verbose_name_plural': '\u8f6e\u64ad\u7ba1\u7406',
            },
        ),
    ]
