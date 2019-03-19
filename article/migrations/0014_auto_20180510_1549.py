# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20180421_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-publish_time'], 'verbose_name': '\u6587\u7ae0'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': '\u6587\u7ae0\u4f5c\u8005'},
        ),
        migrations.AlterModelOptions(
            name='classification',
            options={'verbose_name': '\u6587\u7ae0\u5206\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='messages',
            options={'verbose_name': '\u8bfb\u8005\u7559\u8a00'},
        ),
        migrations.AlterModelOptions(
            name='ownermessage',
            options={'verbose_name': '\u4e3b\u4eba\u5bc4\u8bed'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u6587\u7ae0\u6807\u7b7e'},
        ),
    ]
