# Generated by Django 3.2 on 2021-07-27 10:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0046_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='received',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='принят'),
        ),
    ]
