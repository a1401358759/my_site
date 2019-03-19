# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0020_auto_20181212_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownermessage',
            name='summary',
            field=models.CharField(max_length=100, null=True, verbose_name='\u7b80\u4ecb', blank=True),
        ),
    ]
