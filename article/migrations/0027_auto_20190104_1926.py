# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0026_auto_20190104_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='links',
            name='avatar',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u7f51\u7ad9\u56fe\u6807', blank=True),
        ),
        migrations.AlterField(
            model_name='links',
            name='desc',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u7f51\u7ad9\u63cf\u8ff0', blank=True),
        ),
    ]
