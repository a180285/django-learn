# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_platform_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='interest_manage_rate',
            field=models.FloatField(default=0.0),
        ),
    ]
