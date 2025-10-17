from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('description/', views.description, name='description'),  # Страница "Описание"
    path('feelings/', views.feelings_list, name='feelings_list'),  # Список чувств
    path('feelings/<int:feeling_id>/', views.feeling_detail, name='feeling_detail'),  # Детали чувства



]
