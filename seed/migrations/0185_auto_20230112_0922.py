# Generated by Django 3.2.13 on 2023-01-12 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0184_alter_meter_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='project',
            name='property_views',
        ),
        migrations.RemoveField(
            model_name='project',
            name='super_organization',
        ),
        migrations.RemoveField(
            model_name='project',
            name='taxlot_views',
        ),
        migrations.AlterUniqueTogether(
            name='projectpropertyview',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='projectpropertyview',
            name='approver',
        ),
        migrations.RemoveField(
            model_name='projectpropertyview',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectpropertyview',
            name='property_view',
        ),
        migrations.AlterUniqueTogether(
            name='projecttaxlotview',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='projecttaxlotview',
            name='approver',
        ),
        migrations.RemoveField(
            model_name='projecttaxlotview',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecttaxlotview',
            name='taxlot_view',
        ),
        migrations.DeleteModel(
            name='Compliance',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='ProjectPropertyView',
        ),
        migrations.DeleteModel(
            name='ProjectTaxLotView',
        ),
    ]