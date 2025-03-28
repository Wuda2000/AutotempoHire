# Generated by Django 5.1.7 on 2025-03-20 12:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='id',
        ),
        migrations.AddField(
            model_name='trip',
            name='arrival_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='trip',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='trip',
            name='departure_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='trip',
            name='trip_id',
            field=models.CharField(default='123456abcdef', editable=False, max_length=12, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]
