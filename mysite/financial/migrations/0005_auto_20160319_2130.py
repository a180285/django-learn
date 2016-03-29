# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_auto_20160319_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrecord',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial.UserAccount'),
        ),
    ]