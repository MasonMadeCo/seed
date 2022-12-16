# Generated by Django 3.2.16 on 2022-12-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0182_alter_meter_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compliancemetric',
            name='emission_metric_type',
            field=models.IntegerField(blank=True, choices=[(0, ''), (1, 'Target > Actual for Compliance'), (2, 'Target < Actual for Compliance')], null=True),
        ),
        migrations.AlterField(
            model_name='compliancemetric',
            name='energy_metric_type',
            field=models.IntegerField(blank=True, choices=[(0, ''), (1, 'Target > Actual for Compliance'), (2, 'Target < Actual for Compliance')], null=True),
        ),
    ]
