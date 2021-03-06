# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-25 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('price', models.FloatField(default=0, verbose_name='价格')),
                ('img', models.ImageField(upload_to='', verbose_name='图片')),
                ('create_time', models.DateField(verbose_name='添加时间')),
                ('store', models.IntegerField(default=0, verbose_name='库存')),
                ('desc', models.TextField(verbose_name='描述')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Category')),
            ],
            options={
                'verbose_name_plural': '商品信息',
                'verbose_name': '商品信息',
            },
        ),
        migrations.CreateModel(
            name='GoodsExt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128, verbose_name='属性名')),
                ('value', models.TextField(verbose_name='属性值')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
            ],
            options={
                'verbose_name_plural': '商品扩展信息',
                'verbose_name': '商品扩展信息',
            },
        ),
    ]
