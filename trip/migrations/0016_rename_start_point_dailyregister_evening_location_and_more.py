# Generated by Django 4.2.4 on 2023-10-17 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0015_dailyregister_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailyregister',
            old_name='start_point',
            new_name='evening_location',
        ),
        migrations.RenameField(
            model_name='dailyregister',
            old_name='stop_point',
            new_name='morning_location',
        ),
    ]
