# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20141027_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='abuse',
            name='center_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
