# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0028_auto_20190213_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carouselimg',
            old_name='_type',
            new_name='img_type',
        ),
    ]
