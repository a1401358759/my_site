# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0027_auto_20190104_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselimg',
            name='_type',
            field=models.SmallIntegerField(default=1, verbose_name='\u7c7b\u578b', choices=[(1, 'banner'), (2, 'ads')]),
        ),
        migrations.AlterField(
            model_name='carouselimg',
            name='link',
            field=models.CharField(default=b'', max_length=200, null=True, verbose_name='\u56fe\u7247\u5916\u94fe', blank=True),
        ),
    ]
