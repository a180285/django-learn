# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lianjia', '0013_auto_20170226_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresalePermit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_link', models.URLField(default='', unique=True)),
                ('title', models.CharField(max_length=1024)),
                ('company', models.CharField(max_length=1024)),
                ('location', models.CharField(max_length=1024)),
                ('permit_name', models.CharField(max_length=1024)),
                ('permit_type', models.CharField(max_length=1024)),
                ('date', models.CharField(max_length=1024)),
            ],
        ),
    ]
