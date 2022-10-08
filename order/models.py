from django.db import models
from django.contrib.auth.models import User
from recipes.models import FoodCategory


def get_default_category():
    return FoodCategory.objects.get(title='Классическое')


class Order(models.Model):
    ONEMONTH = 1
    THREEMONTH = 3
    SIXMONTH = 6
    TWELVEMONTH = 12
    TIME_CHOICES = [
        (ONEMONTH, '1 месяц'),
        (THREEMONTH, '3 месяца'),
        (SIXMONTH, '6 месяцев'),
        (TWELVEMONTH, '12 месяцев'),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="orders",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="orders",
        blank=True,
        default=get_default_category
    )
    time = models.PositiveIntegerField(
        verbose_name="Срок заказа в месяцах",
        default=1,
    )
    breakfast = models.BooleanField(
        verbose_name="Завтраки",
        default=True,
    )
    lunch = models.BooleanField(
        verbose_name="Обеды",
        default=True,
    )
    dinner = models.BooleanField(
        verbose_name="Ужины",
        default=True,
    )
    dessert = models.BooleanField(
        verbose_name="Десерты",
        default=True,
    )
    amount_person = models.PositiveIntegerField(
        verbose_name="Количество персон",
        default=1,
    )
    food_form_cost = models.PositiveIntegerField(
        verbose_name="Цена сета для юзера",
        default=100,
    )
    result = models.PositiveIntegerField(
        verbose_name="Итоговая цена",
        default=200,
    )
    is_paid = models.BooleanField(
        verbose_name="Оплачен",
        default=False,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user} - {self.category}"


class Promocode(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=200,
    )
    promocode = models.CharField(
        verbose_name="Промокод",
        max_length=200,
        unique=True
    )
    discount = models.PositiveIntegerField(
        verbose_name="Скидка в процентах",
    )

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.title
