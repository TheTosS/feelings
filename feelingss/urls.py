from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # Сброс пароля
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', views.index, name='home'),
    path('description/', views.description, name='description'),  # Страница "Описание"
    path('feelings/', views.feelings_list, name='feelings_list'),  # Список чувств
    path('feelings/<int:feeling_id>/', views.feeling_detail, name='feeling_detail'),  # Детали чувства

    path('profile/', views.profile, name='profile'),

]
