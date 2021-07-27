# Generated by Django 3.2 on 2021-07-27 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20210727_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(blank=True, choices=[('Card', 'Картой'), ('Cash', 'Наличными')], max_length=10, verbose_name='способ оплаты'),
        ),
    ]
