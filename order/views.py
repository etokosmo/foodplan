from django import forms
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render

from recipes.models import FoodCategory, AllergyCategory
from .models import Promocode, Order


class OrderForm(forms.Form):
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
    TRUE_VALUE = 50
    FALSE_VALUE = 0
    BOOL_CHOICES = [
        (TRUE_VALUE, '✔'),
        (FALSE_VALUE, '✘'),
    ]
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    PERSON_AMOUNT = [
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5'),
        (SIX, '6'),
    ]
    time = forms.ChoiceField(choices=TIME_CHOICES,
                             widget=forms.Select(
                                 attrs={'class': 'form-select',
                                        'onchange': 'submit();'}))
    breakfast = forms.ChoiceField(choices=BOOL_CHOICES,
                                  widget=forms.Select(
                                      attrs={'class': 'form-select',
                                             'onchange': 'submit();'}))
    lunch = forms.ChoiceField(choices=BOOL_CHOICES,
                              widget=forms.Select(
                                  attrs={'class': 'form-select',
                                         'onchange': 'submit();'}))
    dinner = forms.ChoiceField(choices=BOOL_CHOICES,
                               widget=forms.Select(
                                   attrs={'class': 'form-select',
                                          'onchange': 'submit();'}))
    dessert = forms.ChoiceField(choices=BOOL_CHOICES,
                                widget=forms.Select(
                                    attrs={'class': 'form-select',
                                           'onchange': 'submit();'}))
    amount_person = forms.ChoiceField(choices=PERSON_AMOUNT,
                                      widget=forms.Select(
                                          attrs={'class': 'form-select',
                                                 'onchange': 'submit();'}))
    milk_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))
    nuts_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))
    honey_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))
    cereal_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))
    meat_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))
    fish_allergy = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input me-1 foodplan_checked-green',
                   'onchange': 'submit();'}))


class PromoForm(forms.Form):
    promocode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control me-2'}))


class FoodCategoryForm(forms.Form):
    CLASSIC = 100
    LOWCARB = 200
    VEGETERIAN = 300
    KETO = 400
    FOOD_CHOICES = [
        (CLASSIC, 'Классическое'),
        (LOWCARB, 'Низкокалорийное'),
        (VEGETERIAN, 'Вегетарианское '),
        (KETO, 'Кето'),
    ]
    food_category = forms.ChoiceField(choices=FOOD_CHOICES,
                                      widget=forms.RadioSelect(
                                          attrs={'name': 'foodtype',
                                                 'class': 'foodplan_selected d-none',
                                                 'onchange': 'submit(); changeMilk(this);'}))


def create_order(request):
    if request.user.is_anonymous:
        return render(request, 'account/login.html')
    logged_user = request.user
    order, created = Order.objects.get_or_create(user=logged_user)
    if order.is_paid:
        return redirect('/profile')
    user_promocode = ""
    correct_promocode = False

    form = OrderForm(request.POST or None)
    promo_form = PromoForm(request.POST or None)
    food_form = FoodCategoryForm(request.POST or None)
    if food_form.is_valid():
        food_form_cost = int(food_form.cleaned_data.get("food_category"))
        if food_form_cost == 100:
            order.category = FoodCategory.objects.get(title='Классическое')
        if food_form_cost == 200:
            order.category = FoodCategory.objects.get(title='Низкокалорийное')
        if food_form_cost == 300:
            order.category = FoodCategory.objects.get(title='Вегетарианское')
        if food_form_cost == 400:
            order.category = FoodCategory.objects.get(title='Кето')
        order.food_form_cost = food_form_cost
        order.save()
    if form.is_valid():
        order.time = form.cleaned_data.get("time")
        breakfast = form.cleaned_data.get("breakfast")
        if breakfast == '0':
            order.breakfast = False
        else:
            order.breakfast = True
        lunch = form.cleaned_data.get("lunch")
        if lunch == '0':
            order.lunch = False
        else:
            order.lunch = True
        dinner = form.cleaned_data.get("dinner")
        if dinner == '0':
            order.dinner = False
        else:
            order.dinner = True
        dessert = form.cleaned_data.get("dessert")
        if dessert == '0':
            order.dessert = False
        else:
            order.dessert = True
        order.amount_person = form.cleaned_data.get("amount_person")
        order.result = int(order.time) * int(order.amount_person) * (
                int(order.breakfast) * 50 +
                int(order.lunch) * 50 +
                int(order.dinner) * 50 +
                int(order.dessert) * 50
        )
        milk_allergy = form.cleaned_data.get("milk_allergy")
        nuts_allergy = form.cleaned_data.get("nuts_allergy")
        honey_allergy = form.cleaned_data.get("honey_allergy")
        cereal_allergy = form.cleaned_data.get("cereal_allergy")
        meat_allergy = form.cleaned_data.get("meat_allergy")
        fish_allergy = form.cleaned_data.get("fish_allergy")
        milk_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Молочные продукты")
        nuts_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Орехи и бобовые")
        honey_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Продукты пчеловодства")
        cereal_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Зерновые")
        meat_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Мясо")
        fish_allergy_obj, created = AllergyCategory.objects.get_or_create(
            title=
            "Рыба и морепродукты")
        if milk_allergy:
            order.allergies.add(milk_allergy_obj)
        else:
            if milk_allergy_obj in order.allergies.all():
                order.allergies.remove(milk_allergy_obj)
        if nuts_allergy:
            order.allergies.add(nuts_allergy_obj)
        else:
            if nuts_allergy_obj in order.allergies.all():
                order.allergies.remove(nuts_allergy_obj)
        if honey_allergy:
            order.allergies.add(honey_allergy_obj)
        else:
            if honey_allergy_obj in order.allergies.all():
                order.allergies.remove(honey_allergy_obj)
        if cereal_allergy:
            order.allergies.add(cereal_allergy_obj)
        else:
            if cereal_allergy_obj in order.allergies.all():
                order.allergies.remove(cereal_allergy_obj)
        if meat_allergy:
            order.allergies.add(meat_allergy_obj)
        else:
            if meat_allergy_obj in order.allergies.all():
                order.allergies.remove(meat_allergy_obj)
        if fish_allergy:
            order.allergies.add(fish_allergy_obj)
        else:
            if fish_allergy_obj in order.allergies.all():
                order.allergies.remove(fish_allergy_obj)
        order.save()
    if promo_form.is_valid():
        try:
            user_promocode = promo_form.cleaned_data.get("promocode")
            try:
                promocode = Promocode.objects.get(promocode=user_promocode)
                discount = promocode.discount / 100
                order.result = order.result - order.result * discount

                correct_promocode = True
            except Promocode.DoesNotExist:
                pass
        except AttributeError:
            pass

    order.result += order.food_form_cost
    order.save()

    context = {'form': form,
               'promo_form': promo_form,
               'food_form': food_form,
               'result': order.result,
               'time': order.time,
               'breakfast': order.breakfast,
               'lunch': order.lunch,
               'dinner': order.dinner,
               'dessert': order.dessert,
               'amount_person': order.amount_person,
               'promocode': user_promocode,
               'correct_promocode': correct_promocode,
               'food_form_cost': order.food_form_cost,
               'SBOL_SECRET_TOKEN': settings.SBOL_SECRET_TOKEN,
               }

    return render(request, 'order/order.html', context=context)


def success_payment(request):
    logged_user = request.user
    order = Order.objects.get(user=logged_user)
    order.is_paid = True
    order.save()
    return redirect('/profile')
