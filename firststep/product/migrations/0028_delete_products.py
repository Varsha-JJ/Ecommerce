# Generated by Django 4.1.2 on 2023-02-25 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_remove_product_user_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Products',
        ),
    ]
