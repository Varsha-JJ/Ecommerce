# Generated by Django 4.1.2 on 2023-03-07 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0045_alter_orderplaced_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.cart'),
        ),
    ]
