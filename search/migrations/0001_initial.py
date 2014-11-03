# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('roadAddress', models.CharField(max_length=250, null=True, blank=True)),
                ('centerName', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
