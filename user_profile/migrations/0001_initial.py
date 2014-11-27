# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user_profile.models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about_me', models.CharField(max_length=350, verbose_name=b'About me', blank=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2014, 11, 16, 11, 55, 24, 516310))),
                ('profile_picture', models.ImageField(upload_to=user_profile.models.profile_picture_folder, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
            bases=(models.Model,),
        ),
    ]
