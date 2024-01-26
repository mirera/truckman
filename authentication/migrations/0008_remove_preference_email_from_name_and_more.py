# Generated by Django 4.2.4 on 2024-01-08 16:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_client_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='email_from_name',
        ),
        migrations.RemoveField(
            model_name='preference',
            name='from_email',
        ),
        migrations.CreateModel(
            name='EmailSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('email_from_name', models.CharField(max_length=12, null=True)),
                ('from_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('smtp_host', models.CharField(blank=True, max_length=200, null=True)),
                ('encryption', models.CharField(choices=[('tls', 'TLS'), ('ssl', 'SSL'), ('none', 'NONE')], default='tls', max_length=10)),
                ('smtp_port', models.IntegerField(blank=True, null=True)),
                ('smtp_username', models.EmailField(blank=True, max_length=254, null=True)),
                ('smtp_password', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.client')),
            ],
        ),
    ]