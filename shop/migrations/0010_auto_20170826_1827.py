# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-26 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20170817_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='/home/jeongseunghwan/django/hanium/media/default.jpeg', upload_to=''),
        ),
    ]