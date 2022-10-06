import os
from urllib.parse import urlsplit, unquote_plus

import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, URLField, \
    PrimaryKeyRelatedField

from .models import FoodCategory, Recipe, Ingredient, RecipeIngredient, Period


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title']


class RecipeIngredientSerializer(ModelSerializer):
    ingredient = IngredientSerializer(
        many=True,
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'weight_type']


class FoodCategorySerializer(ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ['title']


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
    food_category = PrimaryKeyRelatedField(
        many=True,
        required=True,
        queryset=FoodCategory.objects.all()
    )
    period = PrimaryKeyRelatedField(
        many=True,
        required=True,
        queryset=Period.objects.all()
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

    response = requests.get(recipe_image_url)
    response.raise_for_status()
    uploaded_photo = ContentFile(response.content, name=filename)
    recipe.image = uploaded_photo
    recipe.save()


@api_view(['POST'])
def create_recipe(request):
    serializer = RecipeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    recipe = Recipe.objects.create(
        title=serializer.validated_data['title'],
        recipe=serializer.validated_data['recipe'],
        new_year_tag=serializer.validated_data['new_year_tag'],
        calories=serializer.validated_data['calories'],
        portions=serializer.validated_data['portions'],
        food_category=serializer.validated_data['food_category'][0],
    )
    upload_photo_in_place(recipe, serializer.validated_data['image'])
    for recipe_period in serializer.validated_data['period']:
        recipe.period.add(recipe_period)
    for ingredient in serializer.validated_data['recipe_ingredient']:
        ingredient_title = ingredient.get("ingredient")[0].get("title")
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

    return Response("asd")  # TODO сделать ответ для API


def get_recipe_by_id(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipes/recipe.html', context=context)
