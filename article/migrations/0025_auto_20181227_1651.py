# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0024_music'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='artist',
            field=models.CharField(default=b'', max_length=100, null=True, verbose_name='\u827a\u672f\u5bb6', blank=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='lrc',
            field=models.CharField(default=b'', max_length=100, null=True, verbose_name='\u97f3\u4e50\u6b4c\u8bcd', blank=True),
        ),
    ]
