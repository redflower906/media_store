# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-03 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0052_auto_20190703_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_changed',
            field=models.BooleanField(default=False),
        ),
    ]
