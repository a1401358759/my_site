# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_auto_20180517_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.SmallIntegerField(default=2, verbose_name='\u72b6\u6001', choices=[(1, '\u8349\u7a3f'), (2, '\u5df2\u53d1\u5e03')]),
        ),
    ]
