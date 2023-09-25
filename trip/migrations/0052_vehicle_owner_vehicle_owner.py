# Generated by Django 4.2.4 on 2023-09-25 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_role_name'),
        ('trip', '0051_vehicle_trailer_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle_Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trip.vehicle_owner'),
        ),
    ]
