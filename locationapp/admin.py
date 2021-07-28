from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    fields = ["address", "coordinates", "created_at"]
    search_fields = ["address"]
    list_display = ["address", "coordinates", "created_at"]
    readonly_fields = ["created_at"]
