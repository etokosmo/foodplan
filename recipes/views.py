import os
from urllib.parse import urlsplit, unquote_plus

import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, URLField, CharField

from .models import FoodCategory, Recipe, Ingredient, RecipeIngredient, Period, \
    AllergyCategory


class RecipeIngredientSerializer(ModelSerializer):
    ingredient = CharField()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'weight_type']


class PeriodSerializer(ModelSerializer):
    class Meta:
        model = Period
        fields = ['period']


class RecipeSerializer(ModelSerializer):
    recipe_ingredient = RecipeIngredientSerializer(
        many=True,
        allow_empty=False,
        write_only=True
    )
    food_category = CharField()
    period = PeriodSerializer(
        many=True,
        allow_empty=False,
        write_only=True
    )
    image = URLField()

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'period', 'recipe', 'new_year_tag',
                  'calories', 'portions', 'recipe_ingredient', 'food_category']

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Recipe.objects.update(**validated_data)


def get_filename(url: str) -> str:
    """Получаем название файла и расширение файла из ссылки"""
    truncated_url = unquote_plus(
        urlsplit(url, scheme='', allow_fragments=True).path)
    _, filename = os.path.split(truncated_url)
    return filename


def upload_photo_in_place(recipe: Recipe,
                          recipe_image_url: str) -> None:
    filename = get_filename(recipe_image_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    response = requests.get(recipe_image_url, headers=headers)
    response.raise_for_status()
    uploaded_photo = ContentFile(response.content, name=filename)
    recipe.image = uploaded_photo
    recipe.save()


@api_view(['POST'])
def create_recipe(request):
    serializer = RecipeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    milk_allergy, created = AllergyCategory.objects.get_or_create(
        title='Молочные продукты')
    milk_allergy_ingredients = (
        'молоко', 'сыр', 'сливки', 'творог', 'йогурт', 'сметана', 'ряженка',
        'масло'
    )
    nuts_allergy, created = AllergyCategory.objects.get_or_create(
        title='Орехи и бобовые')
    nuts_allergy_ingredients = (
        'орех', 'фасол', 'горох', 'фисташк', 'соя', 'нут', 'арахис',
        'миндаль', 'фундук', 'каштан', 'ореш', 'боб'
    )
    honey_allergy, created = AllergyCategory.objects.get_or_create(
        title='Продукты пчеловодства')
    honey_allergy_ingredients = (
        'мед', 'мёд', 'перга', 'воск', 'прополис', 'маточное молоко'
    )
    cereal_allergy, created = AllergyCategory.objects.get_or_create(
        title='Зерновые')
    cereal_allergy_ingredients = (
        'пшеница', 'рожь', 'овес', 'овёс', 'рис', 'кукуруза', 'ячмень',
        'просо', 'гречиха', 'гречка', 'мука'
    )
    meat_allergy, created = AllergyCategory.objects.get_or_create(
        title='Мясо')
    meat_allergy_ingredients = (
        'баран', 'свин', 'говядин', 'говяж', 'колбас', 'сосиск', 'паштет',
        'сало', 'сардел', 'тушенка', 'тушёнка'
    )
    fish_allergy, created = AllergyCategory.objects.get_or_create(
        title='Рыба и морепродукты')
    fish_allergy_ingredients = (
        'рыб', 'рак', 'краб', 'креветк', 'омар', 'миди', 'гребеш',
        'кальмар', 'каракатиц', 'карас', 'сибас', 'камбала', 'щук',
        'судак', 'окун', 'горбуш', 'семг', 'сёмг', 'лосос', 'кет',
        'осетр', 'осётр', 'икр'
    )

    food_category, created = FoodCategory.objects.get_or_create(
        title=serializer.validated_data['food_category'])
    recipe, _ = Recipe.objects.get_or_create(
        title=serializer.validated_data['title'],
        defaults={
            'recipe': serializer.validated_data['recipe'],
            'new_year_tag': serializer.validated_data['new_year_tag'],
            'calories': serializer.validated_data['calories'],
            'portions': serializer.validated_data['portions'],
            'food_category': food_category,
        }
    )
    upload_photo_in_place(recipe, serializer.validated_data['image'])
    for recipe_period in serializer.validated_data['period']:
        period, created = Period.objects.get_or_create(
            period=recipe_period.get("period"))
        recipe.period.add(period)
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    for ingredient in serializer.validated_data['recipe_ingredient']:
        ingredient_title = ingredient.get("ingredient")
        ingredient_amount = ingredient.get("amount")
        ingredient_weight_type = ingredient.get("weight_type")
        ingredient_obj, created = Ingredient.objects.get_or_create(
            title=ingredient_title
        )
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient_obj,
            amount=ingredient_amount,
            weight_type=ingredient_weight_type
        )

        if milk_allergy not in recipe.allergy_categories.all():
            for milk_allergy_ingredient in milk_allergy_ingredients:
                if milk_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(milk_allergy)
                    break
        if nuts_allergy not in recipe.allergy_categories.all():
            for nuts_allergy_ingredient in nuts_allergy_ingredients:
                if nuts_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(nuts_allergy)
                    break
        if honey_allergy not in recipe.allergy_categories.all():
            for honey_allergy_ingredient in honey_allergy_ingredients:
                if honey_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(honey_allergy)
                    break
        if cereal_allergy not in recipe.allergy_categories.all():
            for cereal_allergy_ingredient in cereal_allergy_ingredients:
                if cereal_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(cereal_allergy)
                    break
        if meat_allergy not in recipe.allergy_categories.all():
            for meat_allergy_ingredient in meat_allergy_ingredients:
                if meat_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(meat_allergy)
                    break
        if fish_allergy not in recipe.allergy_categories.all():
            for fish_allergy_ingredient in fish_allergy_ingredients:
                if fish_allergy_ingredient in ingredient_title.lower():
                    recipe.allergy_categories.add(fish_allergy)
                    break

    return Response("asd")  # TODO сделать ответ для API


def get_recipe_by_id(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipes/recipe.html', context=context)
