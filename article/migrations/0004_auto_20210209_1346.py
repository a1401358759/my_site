# Generated by Django 3.1.3 on 2021-02-09 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200421_1340'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='article',
            table='article',
        ),
        migrations.AlterModelTable(
            name='author',
            table='author',
        ),
        migrations.AlterModelTable(
            name='carouselimg',
            table='carousel_img',
        ),
        migrations.AlterModelTable(
            name='classification',
            table='classification',
        ),
        migrations.AlterModelTable(
            name='comments',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='links',
            table='links',
        ),
        migrations.AlterModelTable(
            name='music',
            table='music',
        ),
        migrations.AlterModelTable(
            name='ownermessage',
            table='owner_message',
        ),
        migrations.AlterModelTable(
            name='subscription',
            table='subscription',
        ),
        migrations.AlterModelTable(
            name='tag',
            table='tag',
        ),
        migrations.AlterModelTable(
            name='visitor',
            table='visitor',
        ),
    ]
