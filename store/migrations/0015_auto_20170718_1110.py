# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 15:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20170710_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='container',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='inventory_text',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='media_type',
            field=models.CharField(blank=True, choices=[('Agar', 'Agar'), ('Antibiotics', 'Antibiotics'), ('Cornmeal Food', 'Cornmeal Food'), ('Dextrose Food', 'Dextrose Food'), ('Liquid Media', 'Liquid Media'), ('Miscellaneous', 'Miscellaneous'), ('Power Food', 'Power Food'), ('Solutions & Buffers', 'Solutions & Buffers'), ('Sylgard', 'Sylgard'), ('Wurzburg Food', 'Wurzburg Food')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='volume',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
