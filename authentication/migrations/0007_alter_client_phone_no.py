# Generated by Django 4.2.4 on 2023-11-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_whatsappsetting_instance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_no',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
