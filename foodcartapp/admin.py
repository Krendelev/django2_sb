from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse
from django.templatetags.static import static
from django.utils.html import format_html

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
    inlines = [OrderItemInline]

    @admin.display(description="Клиент")
    def get_customer(self, obj):
        return f"{obj.lastname} {obj.firstname}"

    def response_post_save_change(self, request, obj):
        res = super().response_post_save_change(request, obj)
        if "back" in request.GET:
            return redirect("restaurateur:view_orders")
        else:
            return res


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
