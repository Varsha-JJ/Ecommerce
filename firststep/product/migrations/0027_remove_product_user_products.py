# Generated by Django 4.1.2 on 2023-02-25 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0026_alter_product_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('product_image', models.ImageField(unique=True, upload_to='product_image/')),
                ('price', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('description', models.TextField(default='', max_length=1000)),
                ('in_stock', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('color', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.color')),
                ('filterprice', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.filter_price')),
                ('size', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.size')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]