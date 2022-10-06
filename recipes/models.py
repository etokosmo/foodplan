from pathlib import Path

from django.db import models
from tinymce.models import HTMLField


def get_upload_path(instance, filename):
    return Path(instance.title) / filename


class FoodCategory(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Категория Еды'
        verbose_name_plural = 'Категории Еды'

    def __str__(self):
        return self.title


class Period(models.Model):
    period = models.CharField(
        verbose_name="Период приёма пищи",
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Период приёма пищи'
        verbose_name_plural = 'Период приёма пищи'

    def __str__(self):
        return self.period


class Ingredient(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Фотография',
        upload_to=get_upload_path,
        blank=True,
    )
    food_category = models.ForeignKey(
        FoodCategory,
        on_delete=models.CASCADE,
        verbose_name="Категория еды",
        related_name='recipes',
        blank=True,
    )
    recipe = HTMLField(
        verbose_name='Рецепт',
        blank=True,
        null=True
    )
    new_year_tag = models.BooleanField(
        verbose_name='Тэг Новый Год',
        default=False,
    )
    calories = models.PositiveIntegerField(
        verbose_name='Калории',
        blank=True,
        null=True
    )
    portions = models.PositiveIntegerField(
        verbose_name="Порций",
        blank=True,
        null=True,
    )
    period = models.ManyToManyField(
        Period,
        verbose_name="Период приема пищи",
        related_name='recipes',
        blank=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name='ingredients',
        blank=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name='recipes',
        blank=True,
    )
    amount = models.DecimalField(
        verbose_name="Количество",
        max_digits=10,
        decimal_places=1,
        blank=True,
        null=True,
    )
    weight_type = models.CharField(
        verbose_name="Классификация веса",
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Ингредиент в Рецепте'
        verbose_name_plural = 'Ингредиенты в Рецепте'

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"
