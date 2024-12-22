# Generated by Django 5.1.3 on 2024-12-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_products_datetime_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stock',
            field=models.CharField(choices=[('sale', 'sale'), ('soldout', 'soldout')], default='sale', max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('OutForDelivery', 'OutForDelivery'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('OrderPlaced', 'OrderPlaced')], default='OrderPlaced', max_length=100),
        ),
    ]
