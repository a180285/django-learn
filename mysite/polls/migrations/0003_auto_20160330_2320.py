# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-30 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20160330_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='link',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
