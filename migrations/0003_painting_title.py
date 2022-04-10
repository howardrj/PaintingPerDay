# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2022-04-10 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('painting_per_day', '0002_auto_20220410_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='painting',
            name='title',
            field=models.CharField(db_index=True, default='', help_text=b'Title of painting', max_length=400),
            preserve_default=False,
        ),
    ]
