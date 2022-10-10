from django.contrib.auth.models import User
from django.db import models

from recipes.models import FoodCategory, Recipe


def get_default_category():
    return FoodCategory.objects.get(title='Классическое')


class AllergyCategory(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=200,
    )

    class Meta:
        verbose_name = 'Категория Аллергии'
        verbose_name_plural = 'Категории Аллергий'

    def __str__(self):
        return self.title


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
    allergies = models.ForeignKey(
        AllergyCategory,
        on_delete=models.SET_NULL,
        verbose_name="Аллергии",
        related_name="orders",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user} - {self.category}"

    @property
    def amount_meals(self):
        return int(self.breakfast) + int(self.lunch) + int(self.dinner) + int(
            self.dessert)

    def get_day_menu(self, date):
        day_menu, created = DayMenu.objects.get_or_create(
            order=self,
            date=date
        )
        if created:
            day_menu.fill_recipes()
        return day_menu

    def get_description_with_day_menu(self, date):
        day_menu = self.get_day_menu(date)
        calories = (
                (day_menu.breakfast.calories if day_menu.breakfast else 0) +
                (day_menu.lunch.calories if day_menu.lunch else 0) +
                (day_menu.dinner.calories if day_menu.dinner else 0) +
                (day_menu.dessert.calories if day_menu.dessert else 0)
        )
        order = {
            'description': self.category,
            'amount_person': self.amount_person,
            'date': date,
            'breakfast': day_menu.breakfast,
            'lunch': day_menu.lunch,
            'dinner': day_menu.dinner,
            'dessert': day_menu.dessert,
            'amount_meals': self.amount_meals,
            'calories': calories
        }
        return order


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


class DayMenu(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='day_menus'
    )
    date = models.DateField(
        verbose_name='Дата',
    )
    breakfast = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Завтрак',
        related_name='day_menus_breakfast',
        blank=True,
        null=True
    )
    dinner = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Ужин',
        related_name='day_menus_dinner',
        blank=True,
        null=True
    )
    lunch = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Обед',
        related_name='day_menus_lunch',
        blank=True,
        null=True
    )
    dessert = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Десерт',
        related_name='day_menus_dessert',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Меню на день',
        verbose_name_plural = 'Меню на день'

    def fill_recipes(self):
        recipes = Recipe.objects.filter(
            food_category=self.order.category,
            portions__gte=self.order.amount_person,
        ).order_by('?')
        if self.order.breakfast:
            self.breakfast = recipes.filter(
                period__period='Завтрак'
            ).first()
        if self.order.lunch:
            self.lunch = recipes.filter(
                period__period='Обед'
            ).first()
        if self.order.dinner:
            self.dinner = recipes.filter(
                period__period='Ужин'
            ).first()
        if self.order.dessert:
            self.dessert = recipes.filter(
                period__period='Десерт'
            ).first()
        self.save()
