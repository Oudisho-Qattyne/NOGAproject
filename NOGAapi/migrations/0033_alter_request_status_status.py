# Generated by Django 5.0.6 on 2024-08-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0032_alter_user_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request_status',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]
