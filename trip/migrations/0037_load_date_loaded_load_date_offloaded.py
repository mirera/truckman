# Generated by Django 4.2.4 on 2023-11-16 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0036_alter_trip_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='load',
            name='date_loaded',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='load',
            name='date_offloaded',
            field=models.DateField(null=True),
        ),
    ]