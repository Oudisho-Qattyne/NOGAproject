# Generated by Django 5.0.6 on 2024-07-29 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0024_rename_transported_products_transported_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accessory',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='branch_products',
            old_name='branch_id',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='branch_products',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='entered_product',
            old_name='process_id',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='entered_product',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='phone',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='phone_cameras',
            old_name='product_id',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='phones_accessories',
            old_name='accessor_id',
            new_name='accessor',
        ),
        migrations.RenameField(
            model_name='phones_accessories',
            old_name='phone_id',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='products_movment',
            old_name='branch_id',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='transported_product',
            old_name='process_id',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='transported_product',
            old_name='product_id',
            new_name='product',
        ),
    ]
