# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0025_auto_20181227_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='avatar',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u7f51\u7ad9\u56fe\u6807'),
        ),
        migrations.AddField(
            model_name='links',
            name='desc',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u7f51\u7ad9\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='links',
            name='link',
            field=models.CharField(max_length=100, verbose_name='\u7f51\u7ad9\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='links',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u7f51\u7ad9\u540d\u79f0'),
        ),
    ]
