# Generated by Django 4.2.4 on 2023-10-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0006_alter_route_distance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='estimated_duration',
        ),
        migrations.AddField(
            model_name='route',
            name='duration',
            field=models.IntegerField(null=True),
        ),

    ]
