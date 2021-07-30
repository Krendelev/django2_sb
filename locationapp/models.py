from django.db import models
from django.utils import timezone
from geopy.geocoders import Yandex
from star_burger.settings import GEOCODER_API_KEY


class Location(models.Model):
    address = models.CharField("адрес", max_length=100, unique=True)
    coordinates = models.CharField("координаты", max_length=40, blank=True)
    created_at = models.DateTimeField("записано", default=timezone.now)

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "места"

    def __str__(self):
        return f"{self.address}"

    def get_coordinates(address):
        coder = Yandex(GEOCODER_API_KEY)
        location = coder.geocode(address, exactly_one=True)
        return f"{location.point}"

    # def save(self, *args, **kwargs):
    #     self.coordinates = get_coordinates(self.address)
    #     super().save(*args, **kwargs)
