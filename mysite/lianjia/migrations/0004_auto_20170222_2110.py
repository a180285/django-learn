# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0003_secondhandhouse_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondhandhouse',
            name='area',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='secondhandhouse',
            name='building_year',
            field=models.IntegerField(default=0),
        ),
    ]
