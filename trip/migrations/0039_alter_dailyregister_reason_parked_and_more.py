# Generated by Django 4.2.4 on 2023-12-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0038_vehicle_tracking_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyregister',
            name='reason_parked',
            field=models.CharField(blank=True, choices=[('Traffic', 'Traffic'), ('Fuel', 'Fuel'), ('Arrested', 'Arrested'), ('Missing Documentation ', 'Missing Documentation'), ('Missing Documentation Client Side', 'Missing Documentation Client Side')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dailyregister',
            name='vehicle_status',
            field=models.CharField(choices=[('Parked', 'Parked'), ('Moving', 'Moving')], max_length=50),
        ),
    ]
