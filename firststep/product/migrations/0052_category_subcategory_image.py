# Generated by Django 4.1.2 on 2023-03-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0051_maincategory_category_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subcategory_image',
            field=models.ImageField(blank=True, null=True, upload_to='category_image/'),
        ),
    ]
