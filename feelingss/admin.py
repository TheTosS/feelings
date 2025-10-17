from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Feeling  # Импортируйте свою модель

# Регистрируем модель в админке
admin.site.register(Feeling)
