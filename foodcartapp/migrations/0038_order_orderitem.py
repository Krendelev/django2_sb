# Generated by Django 3.2 on 2021-07-25 10:36

from django.db import migrations, models
import django.db.models.deletion
import foodcartapp.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("foodcartapp", "0037_auto_20210125_1833"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=100, verbose_name="адрес")),
                ("first_name", models.CharField(max_length=20, verbose_name="имя")),
                ("last_name", models.CharField(max_length=20, verbose_name="фамилия")),
                (
                    "customer_phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="телефон"
                    ),
                ),
            ],
            options={
                "verbose_name": "заказ",
                "verbose_name_plural": "заказы",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="foodcartapp.order",
                        verbose_name="позиция заказа",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        on_delete=models.PROTECT,
                        related_name="product_orders",
                        to="foodcartapp.product",
                        verbose_name="продукт",
                    ),
                ),
            ],
            options={
                "verbose_name": "позиция заказа",
                "verbose_name_plural": "позиции заказа",
            },
        ),
    ]
