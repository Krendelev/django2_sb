from django.contrib import admin
from django.shortcuts import redirect, reverse
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme
from star_burger.settings import ALLOWED_HOSTS

from .models import (
    Banner,
    Order,
    OrderItem,
    Product,
    ProductCategory,
    Restaurant,
    RestaurantMenuItem,
)


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
        "address",
        "contact_phone",
    ]
    list_display = [
        "name",
        "address",
        "contact_phone",
    ]
    inlines = [RestaurantMenuItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "get_image_list_preview",
        "name",
        "category",
        "price",
    ]
    list_display_links = [
        "name",
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        "name",
        "category__name",
    ]

    inlines = [RestaurantMenuItemInline]
    fieldsets = (
        (
            "Общее",
            {
                "fields": [
                    "name",
                    "category",
                    "image",
                    "get_image_preview",
                    "price",
                ]
            },
        ),
        (
            "Подробно",
            {
                "fields": [
                    "special_status",
                    "description",
                ],
                "classes": ["wide"],
            },
        ),
    )

    readonly_fields = [
        "get_image_preview",
    ]

    class Media:
        css = {"all": (static("admin/foodcartapp.css"))}

    def get_image_preview(self, obj):
        if not obj.image:
            return "выберите картинку"
        return format_html(
            '<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url
        )

    get_image_preview.short_description = "превью"

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return "нет картинки"
        edit_url = reverse("admin:foodcartapp_product_change", args=(obj.id,))
        return format_html(
            '<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>',
            edit_url=edit_url,
            src=obj.image.url,
        )

    get_image_list_preview.short_description = "превью"


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = [
        "firstname",
        "lastname",
        "phonenumber",
        "address",
        "payment",
        "status",
        "received",
        "confirmed",
        "delivered",
        "comment",
        "restaurant",
    ]
    search_fields = [
        "lastname",
        "address",
        "phonenumber",
    ]
    list_display = [
        "get_customer",
        "address",
        "phonenumber",
    ]
    readonly_fields = ["received"]
    inlines = [OrderItemInline]

    @admin.display(description="Клиент")
    def get_customer(self, obj):
        return f"{obj.lastname} {obj.firstname}"

    def response_post_save_change(self, request, obj):
        fallback = super().response_post_save_change(request, obj)
        redirect_to = request.GET.get("next")
        url_is_safe = url_has_allowed_host_and_scheme(
            redirect_to,
            ALLOWED_HOSTS,
            require_https=request.is_secure(),
        )
        if redirect_to and url_is_safe:
            return redirect(redirect_to)
        else:
            return fallback


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
