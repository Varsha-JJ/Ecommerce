# Generated by Django 4.1.2 on 2023-03-08 06:00

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0048_orderplaced_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='products_image',
            field=models.ImageField(default='', upload_to='sell_image/'),
        ),
    ]
