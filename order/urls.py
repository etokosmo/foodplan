from django.urls import path

from .views import create_order, success_payment

app_name = "order"

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('success_payment/', success_payment, name='success_payment'),
]
