# Generated by Django 5.1.7 on 2025-03-21 02:14

import trips.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_remove_trip_id_trip_arrival_time_trip_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_id',
            field=models.CharField(default=trips.models.generate_unique_id, editable=False, max_length=12, primary_key=True, serialize=False, unique=True),
        ),
    ]
