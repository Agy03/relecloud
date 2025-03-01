# Generated by Django 5.1.2 on 2024-10-12 09:27

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0002_cruise_image_destination_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cruise',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='static/cruises'), upload_to='cruises/'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='static/cruises'), upload_to='destinations/'),
        ),
    ]
