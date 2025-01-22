# Generated by Django 5.1.2 on 2024-10-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cruise',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cruises/'),
        ),
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='destinations/'),
        ),
    ]
