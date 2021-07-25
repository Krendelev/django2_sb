import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.templatetags.static import static


from .models import Banner, Product, Order, OrderItem


def banners_list_api(request):
    banners = [
        {"title": obj.title, "src": obj.image.url, "text": obj.tagline}
        for obj in Banner.objects.all()
    ]
    return JsonResponse(
        banners, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4}
    )


def product_list_api(request):
    products = Product.objects.select_related("category").available()

    dumped_products = []
    for product in products:
        dumped_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "special_status": product.special_status,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
            },
            "image": product.image.url,
            "restaurant": {
                "id": product.id,
                "name": product.name,
            },
        }
        dumped_products.append(dumped_product)
    return JsonResponse(
        dumped_products,
        safe=False,
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
        },
    )


def register_order(request):
    try:
        order_serialized = json.loads(request.body.decode())
    except ValueError:
        return HttpResponseBadRequest

    order = Order.objects.create(
        first_name=order_serialized["firstname"],
        last_name=order_serialized["lastname"],
        address=order_serialized["address"],
        customer_phone=order_serialized["phonenumber"],
    )
    for item in order_serialized["products"]:
        OrderItem.objects.get_or_create(
            order=order,
            product=Product.objects.get(pk=item["product"]),
            quantity=item["quantity"],
        )
    return JsonResponse({})
