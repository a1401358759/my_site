# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='content',
            field=models.TextField(max_length=200, verbose_name=b'\xe7\x95\x99\xe8\xa8\x80'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe7\x95\x99\xe8\xa8\x80\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='messages',
            name='email',
            field=models.EmailField(max_length=30, verbose_name=b'\xe9\x82\xae\xe7\xae\xb1'),
        ),
    ]
