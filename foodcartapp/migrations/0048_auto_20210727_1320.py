# Generated by Django 3.2 on 2021-07-27 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_order_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmed',
            field=models.DateTimeField(blank=True, null=True, verbose_name='подтверждён'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered',
            field=models.DateTimeField(blank=True, null=True, verbose_name='доставлен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'Новый'), ('Processing', 'В работе'), ('Delivered', 'Доставка'), ('Cancelled', 'Отменён'), ('Completed', 'Выполнен')], default='New', max_length=10, verbose_name='статус'),
        ),
    ]
