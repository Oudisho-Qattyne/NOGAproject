# Generated by Django 5.0.6 on 2024-05-17 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0003_user_emolyee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='emolyee',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='NOGAapi.employee'),
        ),
    ]