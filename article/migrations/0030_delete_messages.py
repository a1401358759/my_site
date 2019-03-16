# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0029_auto_20190213_1020'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
