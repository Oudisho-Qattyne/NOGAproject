# Generated by Django 5.0.6 on 2024-07-05 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0012_rename_useremployee_user_employee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phone',
            old_name='color',
            new_name='color_id',
        ),
    ]