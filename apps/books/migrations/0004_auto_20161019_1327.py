# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20161019_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(max_length=2000),
        ),
    ]
