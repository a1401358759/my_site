# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_auto_20180510_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-publish_time'], 'verbose_name_plural': '\u6587\u7ae0'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name_plural': '\u6587\u7ae0\u4f5c\u8005'},
        ),
        migrations.AlterModelOptions(
            name='classification',
            options={'verbose_name_plural': '\u6587\u7ae0\u5206\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='messages',
            options={'verbose_name_plural': '\u8bfb\u8005\u7559\u8a00'},
        ),
        migrations.AlterModelOptions(
            name='ownermessage',
            options={'verbose_name_plural': '\u4e3b\u4eba\u5bc4\u8bed'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '\u6587\u7ae0\u6807\u7b7e'},
        ),
    ]
