# Generated by Django 3.2 on 2021-07-29 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveSmallIntegerField(verbose_name='количество'),
        ),
    ]
