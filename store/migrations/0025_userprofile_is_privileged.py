# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-14 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20171114_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_privileged',
            field=models.BooleanField(default=False),
        ),
    ]
