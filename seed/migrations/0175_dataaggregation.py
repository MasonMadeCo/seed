# Generated by Django 3.2.13 on 2022-06-24 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0020_rename_display_significant_figures_organization_display_decimal_places'),
        ('seed', '0174_fix_ghg_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAggregation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.IntegerField(choices=[(0, 'Average'), (1, 'Count'), (2, 'Max'), (3, 'Min'), (4, 'Sum')])),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.column')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.organization')),
            ],
        ),
    ]