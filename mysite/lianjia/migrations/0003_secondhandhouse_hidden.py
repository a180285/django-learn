# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0002_secondhandhouse_like_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='secondhandhouse',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
