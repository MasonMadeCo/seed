# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-09 03:02
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_importer', '0009_importfile_uploaded_filename'),
        ('seed', '0059_auto_20170407_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='import_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_importer.ImportFile'),
        ),
    ]
