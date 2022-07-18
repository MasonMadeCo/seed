# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-07 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_importer', '0011_auto_20180725_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importfile',
            name='export_file',
            field=models.FileField(blank=True, null=True, upload_to='data_imports/exports'),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='file',
            field=models.FileField(blank=True, max_length=500, null=True, upload_to='data_imports'),
        ),
        migrations.AlterField(
            model_name='importrecord',
            name='app',
            field=models.CharField(default='seed', help_text='The application (e.g., BPD or SEED) for this dataset', max_length=64, verbose_name='Destination App'),
        ),
        migrations.AlterField(
            model_name='importrecord',
            name='name',
            field=models.CharField(blank=True, default='Unnamed Dataset', max_length=255, null=True, verbose_name='Name Your Dataset'),
        ),
        migrations.AlterField(
            model_name='importrecord',
            name='status',
            field=models.IntegerField(choices=[(0, 'Uploading'), (1, 'Machine Mapping'), (2, 'Needs Mapping'), (3, 'Machine Cleaning'), (4, 'Needs Cleaning'), (5, 'Ready to Merge'), (6, 'Merging'), (7, 'Merge Complete'), (8, 'Importing'), (9, 'Live'), (10, 'Unknown'), (11, 'Matching')], default=0),
        ),
        migrations.AlterField(
            model_name='tablecolumnmapping',
            name='app',
            field=models.CharField(default='', max_length=64),
        ),
    ]
