from django.contrib import admin

from .models import Promocode, Order


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
