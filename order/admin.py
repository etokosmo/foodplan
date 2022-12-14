from django.contrib import admin

from .models import Promocode, Order, DayMenu, AllergyCategory


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ["title", "promocode", "discount"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "time", "breakfast", "lunch", "dinner",
                    "dessert", "amount_person", "result", "is_paid"]


@admin.register(DayMenu)
class DayMenuAdmin(admin.ModelAdmin):
    list_display = ["order", "date", "breakfast", "lunch", "dinner", "dessert"]


@admin.register(AllergyCategory)
class AllergyCategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
