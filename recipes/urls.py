from django.urls import path

from .views import create_recipe, get_recipe_by_id

app_name = "recipes"

urlpatterns = [
    path('api/create', create_recipe),
    path('<int:recipe_id>/', get_recipe_by_id, name='recipe_page'),
]
