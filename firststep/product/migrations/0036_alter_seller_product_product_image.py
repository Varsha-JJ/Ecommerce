# Generated by Django 4.1.2 on 2023-02-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_alter_seller_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller_product',
            name='product_image',
            field=models.ImageField(unique=True, upload_to='product_image/'),
        ),
    ]
