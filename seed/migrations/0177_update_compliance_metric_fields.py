# Generated by Django 3.2.14 on 2022-09-07 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0176_compliance_metric'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compliancemetric',
            old_name='metric_type',
            new_name='emission_metric_type',
        ),
        migrations.RemoveField(
            model_name='compliancemetric',
            name='actual_column',
        ),
        migrations.RemoveField(
            model_name='compliancemetric',
            name='target_column',
        ),
        migrations.AddField(
            model_name='compliancemetric',
            name='actual_emission_column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_emission_column', to='seed.column'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compliancemetric',
            name='actual_energy_column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_energy_column', to='seed.column'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compliancemetric',
            name='energy_metric_type',
            field=models.IntegerField(choices=[(0, 'Target > Actual for Compliance'), (1, 'Actual > Target for Compliance')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compliancemetric',
            name='target_emission_column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_emission_column', to='seed.column'),
        ),
        migrations.AddField(
            model_name='compliancemetric',
            name='target_energy_column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_energy_column', to='seed.column'),
        ),
    ]
