# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0017_auto_20160602_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingsnapshot',
            name='recent_sale_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
