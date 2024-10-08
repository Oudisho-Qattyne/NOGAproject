# Generated by Django 5.0.6 on 2024-08-10 15:31

import NOGAapi.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0034_branches_requests_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=NOGAapi.models.upload_to, validators=[NOGAapi.models.validate_image_size]),
        ),
    ]
