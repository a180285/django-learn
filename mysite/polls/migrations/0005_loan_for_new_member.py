# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20160331_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='for_new_member',
            field=models.BooleanField(default=False),
        ),
    ]
