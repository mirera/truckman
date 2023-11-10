# Generated by Django 4.2.4 on 2023-11-09 11:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_customuser_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsappSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('access_token', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
    ]
