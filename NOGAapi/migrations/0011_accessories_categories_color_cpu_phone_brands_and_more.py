# Generated by Django 5.0.6 on 2024-07-05 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOGAapi', '0010_customer_products_categories_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessories_Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CPU_brand', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Phone_Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='city',
            name='city_name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Accessories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.product')),
                ('accessory_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.accessories_categories')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CPU_name', models.CharField(max_length=50)),
                ('RAM', models.IntegerField()),
                ('storage', models.IntegerField()),
                ('battery', models.IntegerField()),
                ('sim', models.IntegerField()),
                ('display_size', models.FloatField()),
                ('sd_card', models.BooleanField()),
                ('description', models.CharField(max_length=200)),
                ('release_date', models.DateField()),
                ('CPU_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.cpu')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.color')),
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.product')),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.phone_brands')),
            ],
        ),
        migrations.CreateModel(
            name='Phone_Accessories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.accessories')),
                ('phone_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.phone')),
            ],
        ),
        migrations.CreateModel(
            name='Phone_Cameras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_resolution', models.FloatField()),
                ('main', models.BooleanField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NOGAapi.phone')),
            ],
        ),
    ]
