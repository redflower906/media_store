# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2023-10-25 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0053_order_is_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='location',
            field=models.CharField(choices=[('1E.372', '1E.372 (21C)'), ('2W.225', '2W.225 (4C)'), ('2W.227', '2W.227 (4C)'), ('2W.263', '2W.263 (4C)'), ('2W.265', '2W.265 (4C)'), ('2C.225', '2C.225 (4C)'), ('2C.227', '2C.227 (4C)'), ('2C.267', '2C.267 (4C)'), ('2C.277', '2C.277 (4C)'), ('2E.231', '2E.231 (4C)'), ('2E.233', '2E.233 (18C)'), ('2E.267', '2E.267 (4C)'), ('2E.336.1', 'Robot Room (21C)'), ('2E.372.1', 'Virus Services (21C)'), ('2W.223', 'Tebo (4C)'), ('3W.228', '3W.228 (4C)'), ('3W ambient', ' Near 3W.248 (21C)'), ('3W.266', '3W.266 (4C)'), ('3C.226', '3C.226 (4C)'), ('3C.229', '3C.229 (18C)'), ('3C.265', '3C.265 (4C)'), ('3C.267', '3C.267 (4C)'), ('3C ambient', 'Near 3C.289 (21C)'), ('3E.265', '3E.265 (18C)'), ('3E.267', '3E.267 (4C)')], max_length=30),
        ),
    ]
