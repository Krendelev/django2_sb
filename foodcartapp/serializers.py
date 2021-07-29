from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ["products", "firstname", "lastname", "phonenumber", "address"]

    def create(self, validated_data):
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        order_items = [
            OrderItem(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price * item["quantity"],
            )
            for item in products
        ]
        OrderItem.objects.bulk_create(order_items)

        return order
