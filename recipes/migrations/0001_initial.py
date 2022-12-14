# Generated by Django 4.1.2 on 2022-10-05 16:45

from django.db import migrations, models
import django.db.models.deletion
import recipes.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория Еды',
                'verbose_name_plural': 'Категории Еды',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(blank=True, upload_to=recipes.models.get_upload_path, verbose_name='Фотография')),
                ('period', models.CharField(choices=[('BF', 'Завтрак'), ('LN', 'Обед'), ('DN', 'Ужин'), ('DS', 'Десерт')], db_index=True, default='DN', max_length=2, verbose_name='Период приёма пищи')),
                ('recipe', tinymce.models.HTMLField(blank=True, null=True, verbose_name='Рецепт')),
                ('new_year_tag', models.BooleanField(default=False, verbose_name='Тэг Новый Год')),
                ('calories', models.PositiveIntegerField(blank=True, null=True, verbose_name='Калории')),
                ('portions', models.PositiveIntegerField(blank=True, null=True, verbose_name='Порций')),
                ('food_category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.foodcategory', verbose_name='Категория еды')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True, verbose_name='Количество')),
                ('weight_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Классификация веса')),
                ('ingredient', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Ингредиент в Рецепте',
                'verbose_name_plural': 'Ингредиенты в Рецепте',
            },
        ),
    ]
