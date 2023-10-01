# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-08 22:21
from __future__ import unicode_literals

import quantityfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0071_auto_20170721_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertystate',
            name='conditioned_floor_area_pint',
            field=quantityfield.fields.QuantityField(base_units='ft**2', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='gross_floor_area_pint',
            field=quantityfield.fields.QuantityField(base_units='ft**2', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='occupied_floor_area_pint',
            field=quantityfield.fields.QuantityField(base_units='ft**2', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='site_eui_pint',
            field=quantityfield.fields.QuantityField(base_units='kBtu/ft**2/year', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='site_eui_weather_normalized_pint',
            field=quantityfield.fields.QuantityField(base_units='kBtu/ft**2/year', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='source_eui_pint',
            field=quantityfield.fields.QuantityField(base_units='kBtu/ft**2/year', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='propertystate',
            name='source_eui_weather_normalized_pint',
            field=quantityfield.fields.QuantityField(base_units='kBtu/ft**2/year', blank=True, null=True),
        ),
    ]
