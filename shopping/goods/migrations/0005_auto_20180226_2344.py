# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-26 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20180226_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Category', verbose_name='商品分类'),
        ),
        migrations.AlterField(
            model_name='goodsext',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品名称'),
        ),
    ]
