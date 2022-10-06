from django.contrib import admin

from .models import FoodCategory, Period, Ingredient, Recipe, RecipeIngredient


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ["pk", "period"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass
