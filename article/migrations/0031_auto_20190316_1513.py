# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0030_delete_messages'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='creat_time',
            new_name='created_time',
        ),
    ]
