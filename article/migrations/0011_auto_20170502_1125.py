# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20160729_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=DjangoUeditor.models.UEditorField(null=True, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='content',
            field=DjangoUeditor.models.UEditorField(max_length=200, verbose_name=b'\xe7\x95\x99\xe8\xa8\x80'),
        ),
        migrations.AlterField(
            model_name='ownermessage',
            name='message',
            field=DjangoUeditor.models.UEditorField(verbose_name=b'\xe5\xaf\x84\xe8\xaf\xad'),
        ),
    ]
