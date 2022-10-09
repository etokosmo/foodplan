from django.contrib import admin

from .models import Promocode, Order


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["title", "promocode", "discount"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "time", "breakfast", "lunch", "dinner",
                    "dessert", "amount_person", "result", "is_paid"]
