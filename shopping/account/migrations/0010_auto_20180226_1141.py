# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-26 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20180225_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userext',
            name='verification_time',
            field=models.IntegerField(default=1519617093.1310236, verbose_name='失效时间'),
        ),
    ]
