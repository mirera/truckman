# Generated by Django 4.2.4 on 2023-10-04 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0008_remove_route_estimated_duration_route_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='distance',
            field=models.IntegerField(null=True),
        ),
    ]
