from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField("название", max_length=50)
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        "контактный телефон",
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = RestaurantMenuItem.objects.filter(availability=True).values_list(
            "product"
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("название", max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="категория",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        "цена", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    image = models.ImageField("картинка")
    special_status = models.BooleanField(
        "спец.предложение",
        default=False,
        db_index=True,
    )
    description = models.TextField(
        "описание",
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="menu_items",
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="продукт",
    )
    availability = models.BooleanField("в продаже", default=True, db_index=True)

    class Meta:
        verbose_name = "пункт меню ресторана"
        verbose_name_plural = "пункты меню ресторана"
        unique_together = [["restaurant", "product"]]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def price(self):
        return self.annotate(
            price=Sum(F("products__quantity") * F("products__product__price"))
        )


class Order(models.Model):
    STATUS_CHOICES = [
        ("New", "Новый"),
        ("Processing", "В работе"),
        ("Delivered", "Доставка"),
        ("Cancelled", "Отменён"),
        ("Completed", "Выполнен"),
    ]
    address = models.CharField("адрес", max_length=100)
    firstname = models.CharField("имя", max_length=20)
    lastname = models.CharField("фамилия", max_length=20)
    phonenumber = PhoneNumberField("телефон")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="New")
    comment = models.TextField(blank=True)

    objects = OrderQuerySet.as_manager()

    class Meta:
        ordering = ["-pk"]
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.address}"


def get_sentinel_product():
    return Product.objects.get_or_create(name="deleted")[0]


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="products",
        verbose_name="позиция заказа",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        blank=True,
        related_name="product_orders",
        verbose_name="продукт",
        on_delete=models.SET(get_sentinel_product),
    )
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(
        "стоимость", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "позиция заказа"
        verbose_name_plural = "позиции заказа"

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Banner(models.Model):
    title = models.CharField(max_length=20)
    tagline = models.CharField(max_length=100)
    image = models.ImageField("фото")

    class Meta:
        verbose_name = "баннер"
        verbose_name_plural = "баннеры"

    def __str__(self):
        return f"{self.title}"
