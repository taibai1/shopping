# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-25 07:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20180224_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userext',
            name='verification_time',
            field=models.IntegerField(default=1519543347.1160676, verbose_name='失效时间'),
        ),
    ]
