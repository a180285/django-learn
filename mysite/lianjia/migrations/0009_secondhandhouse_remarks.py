# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0008_secondhandhouse_rooms_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondhandhouse',
            name='remarks',
            field=models.CharField(default='', max_length=10000),
        ),
    ]