# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0031_auto_20190316_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='editor',
            field=models.SmallIntegerField(default=1, verbose_name='\u7f16\u8f91\u5668\u7c7b\u578b', choices=[(1, '\u5bcc\u6587\u672c\u7f16\u8f91\u5668'), (2, 'Markdown\u7f16\u8f91\u5668')]),
        ),
        migrations.AddField(
            model_name='ownermessage',
            name='editor',
            field=models.SmallIntegerField(default=1, verbose_name='\u7f16\u8f91\u5668\u7c7b\u578b', choices=[(1, '\u5bcc\u6587\u672c\u7f16\u8f91\u5668'), (2, 'Markdown\u7f16\u8f91\u5668')]),
        ),
    ]
