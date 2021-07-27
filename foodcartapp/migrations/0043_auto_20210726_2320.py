# Generated by Django 3.2 on 2021-07-26 20:08

from django.db import migrations


def calculate_price(apps, schema_editor):
    OrderItem = apps.get_model("foodcartapp", "OrderItem")
    for item in OrderItem.objects.all():
        item.price = item.product.price * item.quantity
        item.save(update_fields=["price"])


class Migration(migrations.Migration):

    dependencies = [("foodcartapp", "0041_alter_orderitem_order")]

    operations = [migrations.RunPython(calculate_price)]