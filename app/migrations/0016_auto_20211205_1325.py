# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-05 10:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20211204_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2021, 12, 5, 13, 25, 21, 656069), verbose_name='Опубликован'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2021, 12, 5, 13, 25, 21, 656069), verbose_name='Дата'),
        ),
    ]
