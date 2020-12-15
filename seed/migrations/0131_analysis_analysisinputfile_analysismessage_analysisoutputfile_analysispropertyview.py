# Generated by Django 2.2.13 on 2020-11-25 19:33

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0014_organization_geocoding_enabled'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seed', '0130_auto_20200924_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('service', models.IntegerField(choices=[(1, 'BSyncr')])),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(10, 'Creating'), (20, 'Ready'), (30, 'Queued'), (40, 'Running'), (50, 'Failed'), (60, 'Stopped'), (70, 'Completed')])),
                ('configuration', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('parsed_results', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orgs.Organization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisPropertyView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parsed_results', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.Analysis')),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.Cycle')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.Property')),
                ('property_state', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='seed.PropertyState')),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisOutputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, upload_to='analysis_output_files')),
                ('content_type', models.IntegerField(choices=[(1, 'BuildingSync')])),
                ('analysis_property_views', models.ManyToManyField(to='seed.AnalysisPropertyView')),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'default')])),
                ('user_message', models.CharField(default=None, max_length=255)),
                ('debug_message', models.CharField(blank=True, max_length=255)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.Analysis')),
                ('analysis_property_view', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seed.AnalysisPropertyView')),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisInputFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=500, upload_to='analysis_input_files')),
                ('content_type', models.IntegerField(choices=[(1, 'BuildingSync')])),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.Analysis')),
            ],
        ),
    ]