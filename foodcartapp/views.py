from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Banner, Product, Order, OrderItem


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


def validate_data(data):
    if not all(value for value in data.values()):
        return {"error": "fields cannot be empty"}
    try:
        products = data["products"]
    except KeyError:
        return {"error": "'products' not found in request"}

    if not isinstance(products, list):
        return {"error": "'products' is not list"}

    return None


@api_view(["POST"])
def register_order(request):
    if err := validate_data(request.data):
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        first_name=request.data["firstname"],
        last_name=request.data["lastname"],
        address=request.data["address"],
        customer_phone=request.data["phonenumber"],
    )
    for item in request.data["products"]:
        OrderItem.objects.get_or_create(
            order=order,
            product=Product.objects.get(pk=item["product"]),
            quantity=item["quantity"],
        )
    return Response({}, status=status.HTTP_201_CREATED)
