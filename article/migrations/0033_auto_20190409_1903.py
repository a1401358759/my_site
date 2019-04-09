# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0032_auto_20190317_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9c\x80\xe5\x90\x8e\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4')),
                ('email', models.EmailField(max_length=254, verbose_name='\u8ba2\u9605\u90ae\u7bb1')),
            ],
            options={
                'verbose_name_plural': '\u90ae\u4ef6\u8ba2\u9605',
            },
        ),
        migrations.AddField(
            model_name='links',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='\u8054\u7cfb\u90ae\u7bb1', blank=True),
        ),
    ]
