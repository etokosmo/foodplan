# Generated by Django 4.1.2 on 2022-10-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodcategory',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='period',
            name='period',
            field=models.CharField(max_length=100, unique=True, verbose_name='Период приёма пищи'),
        ),
    ]
