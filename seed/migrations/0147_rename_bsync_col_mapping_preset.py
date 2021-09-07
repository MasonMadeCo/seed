# Generated by Django 2.2.10 on 2020-05-01 21:24

from django.db import migrations


def rename_default_bsync_presets(apps, schema_editor):
    """rename the default BuildingSync column mapping preset for each organization"""
    ColumnMappingProfile = apps.get_model("seed", "ColumnMappingProfile")

    ColumnMappingProfile.objects.filter(name='BuildingSync v2.0 Defaults').update(name='BuildingSync v2 Defaults')


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0146_merge_20210622_2054'),
    ]

    operations = [
        migrations.RunPython(rename_default_bsync_presets),
    ]