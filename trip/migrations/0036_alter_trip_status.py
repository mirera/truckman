# Generated by Django 4.2.4 on 2023-11-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0035_alter_customer_payment_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('Not Started', 'Not Started'), ('Dispatched', 'Dispatched'), ('Completed', 'Completed')], default='Not Started', max_length=30),
        ),
    ]
