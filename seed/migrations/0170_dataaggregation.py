# Generated by Django 3.2.13 on 2022-06-23 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0169_auto_20220616_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAggregation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField(choices=[(0, 'Average'), (1, 'Count'), (2, 'Max'), (3, 'Min'), (4, 'Sum')])),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seed.column')),
            ],
        ),
    ]
