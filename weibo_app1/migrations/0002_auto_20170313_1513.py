# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weibo_app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to="'userimage/{}'.format(name)"),
        ),
    ]