# Generated by Django 5.1.4 on 2024-12-20 18:23

import django.db.models.deletion
import relecloud.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0005_alter_cruise_destinations_alter_cruise_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cruise',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=relecloud.models.AzureMediaStorage(), upload_to='cruises/'),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=relecloud.models.AzureMediaStorage(), upload_to='destinations/'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('cruise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='relecloud.cruise')),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='relecloud.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='relecloud.destination')),
            ],
        ),
    ]
