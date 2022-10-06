from django.db import models

from recipes.models import FoodCategory


class Order(models.Model):
    ONEMONTH = 'OM'
    THREEMONTH = 'TM'
    SIXMONTH = 'SM'
    TWELVEMONTH = 'WM'
    STATUS_CHOICES = [
        (ONEMONTH, '1 месяц'),
        (THREEMONTH, '3 месяца'),
        (SIXMONTH, '6 месяцев'),
        (TWELVEMONTH, '12 месяцев'),
    ]
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="orders"
    )
    time = models.CharField(
        verbose_name="Срок заказа",
        max_length=2,
        choices=STATUS_CHOICES,
        default=ONEMONTH,
        db_index=True
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
