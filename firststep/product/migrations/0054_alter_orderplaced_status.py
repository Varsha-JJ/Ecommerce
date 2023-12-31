# Generated by Django 4.1.2 on 2023-04-02 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0053_remove_category_subcategory_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]
