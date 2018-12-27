# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0022_carouselimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselimg',
            name='link',
            field=models.CharField(default=b'', max_length=200, null=True, verbose_name='\u56fe\u7247\u5916\u94fe'),
        ),
    ]
