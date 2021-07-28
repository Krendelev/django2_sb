from django.db import models
from django.utils import timezone
from environs import Env
from geopy.geocoders import Yandex

env = Env()
env.read_env()


def get_coordinates(address):
    coder = Yandex(env("GEOCODER_API_KEY"))
    _, coordinates = coder.geocode(address, exactly_one=True)
    return str(coordinates)


class Location(models.Model):
    address = models.CharField("адрес", max_length=100, unique=True)
    coordinates = models.CharField("координаты", max_length=30, blank=True)
    created_at = models.DateTimeField("записано", default=timezone.now)

    class Meta:
        verbose_name = "место"
        verbose_name_plural = "места"

    def __str__(self):
        return f"{self.address}"

    def save(self, *args, **kwargs):
        self.coordinates = get_coordinates(self.address)
        super().save(*args, **kwargs)
