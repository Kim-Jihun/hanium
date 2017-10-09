# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-07 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_tag_avg_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1024px-No_image_3x4.svg.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='menu',
            field=models.TextField(default='메뉴 정보 없음', max_length=500, null=True, verbose_name='메뉴 가격'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='avg_price',
            field=models.PositiveIntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='tag',
            name='menu',
            field=models.TextField(default='메뉴정보 없음', max_length=300, verbose_name='메뉴와 가격'),
        ),
    ]