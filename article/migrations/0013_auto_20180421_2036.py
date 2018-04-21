# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20180420_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='created_time',
            new_name='creat_time',
        ),
    ]
