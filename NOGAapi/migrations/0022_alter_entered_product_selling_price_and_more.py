# Generated by Django 5.0.6 on 2024-07-28 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0021_entry_process_entered_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entered_product',
            name='selling_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='entered_product',
            name='wholesale_price',
            field=models.IntegerField(null=True),
        ),
    ]
