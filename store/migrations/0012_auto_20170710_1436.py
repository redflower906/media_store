# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20170707_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='media_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='product',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
