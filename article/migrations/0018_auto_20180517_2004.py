# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_auto_20180515_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u6587\u7ae0\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='content',
            field=models.TextField(default=b'', verbose_name='\u7559\u8a00'),
        ),
        migrations.AlterField(
            model_name='ownermessage',
            name='message',
            field=models.TextField(default=b'', verbose_name='\u5bc4\u8bed'),
        ),
    ]
