# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-20 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weibo_app1', '0008_auto_20170320_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massage',
            name='filecontent',
            field=models.FileField(blank=True, null=True, upload_to='/media//massagefile/'),
        ),
        migrations.AlterField(
            model_name='massage',
            name='imagecontent',
            field=models.ImageField(blank=True, null=True, upload_to='/media//massageimage/'),
        ),
    ]
