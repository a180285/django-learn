# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0011_auto_20170224_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondhandhouse',
            name='remarks',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]