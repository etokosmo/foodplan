# Generated by Django 4.0.1 on 2022-10-09 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_alter_recipeingredient_amount'),
        ('order', '0007_alter_order_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('breakfast', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_menus_breakfast', to='recipes.recipe', verbose_name='Завтрак')),
                ('dessert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_menus_dessert', to='recipes.recipe', verbose_name='Десерт')),
                ('dinner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_menus_dinner', to='recipes.recipe', verbose_name='Ужин')),
                ('lunch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_menus_lunch', to='recipes.recipe', verbose_name='Обед')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_menus', to='order.order', verbose_name='Подписка')),
            ],
            options={
                'verbose_name': 'Меню на день',
            },
        ),
    ]