# Generated by Django 5.0.6 on 2024-08-08 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0033_alter_request_status_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='branches_requests',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]