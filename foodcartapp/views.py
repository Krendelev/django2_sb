from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Banner, Product, Order, OrderItem
from .serializers import OrderSerializer

from pprint import pprint


@api_view(["GET"])
def banners_list_api(request):
    banners = [
        {"title": obj.title, "src": obj.image.url, "text": obj.tagline}
        for obj in Banner.objects.all()
    ]
    return Response(banners)


@api_view(["GET"])
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

    return Response(dumped_products)


@api_view(["POST"])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({}, status=status.HTTP_201_CREATED)
