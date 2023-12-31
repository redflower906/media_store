# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_inventory_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='container',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='inventory_text',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='media_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
