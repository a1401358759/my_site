# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_ownermessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownermessage',
            name='message',
            field=models.TextField(verbose_name=b'\xe5\xaf\x84\xe8\xaf\xad'),
        ),
    ]
