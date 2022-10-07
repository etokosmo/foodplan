from django import forms
from django.shortcuts import render


class UserForm(forms.Form):
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
    person_amount = forms.ChoiceField(choices=PERSON_AMOUNT,
                                      widget=forms.Select(
                                          attrs={'class': 'form-select',
                                                 'onchange': 'submit();'}))


def create_order(request):
    logged_user = request.user

    result = 200
    time = 1
    breakfast = 50
    lunch = 50
    dinner = 50
    dessert = 50
    person_amount = 1

    form = UserForm(request.POST or None)
    if form.is_valid():
        time = form.cleaned_data.get("time")
        breakfast = form.cleaned_data.get("breakfast")
        lunch = form.cleaned_data.get("lunch")
        dinner = form.cleaned_data.get("dinner")
        dessert = form.cleaned_data.get("dessert")
        person_amount = form.cleaned_data.get("person_amount")
        result = int(time) * int(person_amount) * (
            int(breakfast) + int(lunch) + int(dinner) + int(dessert)
        )
    context = {'form': form,
               'result': result,
               'time': time,
               'breakfast': breakfast,
               'lunch': lunch,
               'dinner': dinner,
               'dessert': dessert,
               'person_amount': person_amount,
               }

    return render(request, 'order/order.html', context=context)
