# Generated by Django 4.2.4 on 2023-10-04 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_borderstop_stoppoint_remove_route_stop_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='distance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='estimated_duration',
            field=models.DurationField(null=True),
        ),
    ]