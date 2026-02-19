from django.urls import path
from . import views

urlpatterns = [
    path('<str:dish_name>/', views.dish_view, name='dish_view'),
]