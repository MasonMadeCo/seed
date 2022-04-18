# Generated by Django 3.2.12 on 2022-03-18 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0158_sensorreading'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, max_length=500, null=True, upload_to='inventory_documents')),
                ('file_type', models.IntegerField(choices=[(0, 'Unknown'), (1, 'PDF')], default=0)),
                ('filename', models.CharField(blank=True, max_length=255)),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory_documents', to='seed.property')),
            ],
        ),
    ]
