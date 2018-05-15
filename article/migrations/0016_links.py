# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_auto_20180510_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xe9\x93\xbe\xe6\x8e\xa5\xe5\x90\x8d\xe7\xa7\xb0')),
                ('link', models.CharField(max_length=100, verbose_name=b'\xe9\x93\xbe\xe6\x8e\xa5\xe5\x9c\xb0\xe5\x9d\x80')),
                ('weights', models.SmallIntegerField(default=10, null=True, verbose_name=b'\xe6\x9d\x83\xe9\x87\x8d', blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u53cb\u60c5\u94fe\u63a5',
            },
        ),
    ]
