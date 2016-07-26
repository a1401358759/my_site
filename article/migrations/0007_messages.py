# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20160722_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d')),
                ('email', models.EmailField(max_length=30, verbose_name=b'\xe9\x82\xae\xe4\xbb\xb6')),
                ('content', models.TextField(max_length=200, verbose_name=b'\xe4\xb8\xaa\xe4\xba\xba\xe7\xbd\x91\xe7\xab\x99')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
