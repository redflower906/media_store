# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-07-12 20:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0041_remove_order_recur_stop_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
