from collections import defaultdict
from operator import itemgetter

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from foodcartapp.models import Order, Product, Restaurant, RestaurantMenuItem
from locationapp.models import Location
from geopy import distance, point


class Login(forms.Form):
    username = forms.CharField(
        label="Логин",
        max_length=75,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Укажите имя пользователя"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        max_length=75,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={"form": form})

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(
            request,
            "login.html",
            context={
                "form": form,
                "ivalid": True,
            },
        )


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy("restaurateur:login")


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_products(request):
    restaurants = list(Restaurant.objects.order_by("name"))
    products = list(Product.objects.prefetch_related("menu_items"))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{
                item.restaurant_id: item.availability
                for item in product.menu_items.all()
            },
        }
        orderer_availability = [
            availability[restaurant.id] for restaurant in restaurants
        ]

        products_with_restaurants.append((product, orderer_availability))

    return render(
        request,
        template_name="products_list.html",
        context={
            "products_with_restaurants": products_with_restaurants,
            "restaurants": restaurants,
        },
    )


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_restaurants(request):
    return render(
        request,
        template_name="restaurants_list.html",
        context={"restaurants": Restaurant.objects.all()},
    )


def get_point(coordinates):
    return point.Point.from_string(coordinates)


@user_passes_test(is_manager, login_url="restaurateur:login")
def view_orders(request):
    orders = (
        Order.objects.all()
        .with_price()
        .prefetch_related("order_items", "order_items__product")
    )
    menu_items = RestaurantMenuItem.objects.filter(availability=True).select_related(
        "restaurant", "product"
    )
    locations = Location.objects.values_list("coordinates", flat=True)

    products_in_restaurants = defaultdict(list)
    for item in menu_items:
        products_in_restaurants[item.product].append(item.restaurant)

    for order in orders:
        restaurants = [
            set(products_in_restaurants[item.product])
            for item in order.order_items.all()
        ]

        restaurants_with_distance = []
        customer_location = get_point(locations.get(address=order.address))

        for restaurant in set.intersection(*restaurants):
            restaurant_location = get_point(locations.get(address=restaurant.address))
            dist = distance.distance(customer_location, restaurant_location).km
            restaurants_with_distance.append((restaurant.name, round(dist, 3)))

        order.available_in = sorted(restaurants_with_distance, key=itemgetter(1))

    return render(request, template_name="order_items.html", context={"orders": orders})
