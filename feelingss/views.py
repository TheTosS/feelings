from . import forms
from .forms import CustomUserCreationForm, FeelingForm

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Feeling


def home(request):
    if request.user.is_authenticated:
        feelings = Feeling.objects.filter(user=request.user).order_by('-created_at')

        if request.method == 'POST':
            form = FeelingForm(request.POST)
            if form.is_valid():
                feeling = form.save(commit=False)
                feeling.user = request.user
                feeling.save()
                messages.success(request, '✅ Запись успешно добавлена!')
                return redirect('home')
        else:
            form = FeelingForm()

        return render(request, 'home.html', {
            'feelings': feelings,
            'form': form
        })
    else:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, '🎉 Регистрация прошла успешно!')
                return redirect('home')
        else:
            form = CustomUserCreationForm()

        return render(request, 'home.html', {'form': form})


@login_required
def delete_feeling(request, pk):
    feeling = get_object_or_404(Feeling, pk=pk, user=request.user)
    if request.method == 'POST':
        feeling.delete()
        messages.success(request, '🗑️ Запись удалена!')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def feeling_list(request):
    feelings = Feeling.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = Feeling(request.POST)
        if form.is_valid():
            feeling = form.save()
            feeling.user = request.user
            feeling.save()
            messages.success(request, 'Запись добавлена!')
            return redirect('home')
        else:
            return render(request, 'index.html', {
                'form': form,
                'feelings': feelings,
            })
    else:
        form = Feeling()

    return render(request, 'index.html', {
        'feelings': feelings,
        'form': form
    })



# Защищенные представления
@login_required
def profile(request):
    # Статистика пользователя
    user_feelings = Feeling.objects.filter(user=request.user)
    total_feelings = user_feelings.count()

    # Подсчет эмоций с правильными названиями
    emotion_stats = {}
    for emotion_code, emotion_name in Feeling.EMOTION_CHOICES:
        count = user_feelings.filter(emotion=emotion_code).count()
        if count > 0:
            emotion_stats[emotion_name] = count

    # Последние записи
    recent_feelings = user_feelings.order_by('-created_at')[:5]

    context = {
        'total_feelings': total_feelings,
        'emotion_stats': emotion_stats,
        'recent_feelings': recent_feelings,
    }

    return render(request, 'profile.html', context)


@login_required
def edit_feeling(request, pk):
    feeling = get_object_or_404(Feeling, pk=pk, user=request.user)


def index(request):
    return render(request, 'index.html')


def feelings(request):
    return render(request, 'feelings.html')


def description(request):
    return render(request, 'description.html')


def feelings_list(request):
    feelings = Feeling.objects.all()  # Получаем все чувства из базы
    return render(request, 'feelings_list.html', {'feelings': feelings})

def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('home')
def feeling_detail(request, feeling_id):
    feeling = get_object_or_404(Feeling, id=feeling_id)  # Получаем чувство по id (или 404)
    return render(request, 'feeling_detail.html', {'feeling': feeling})
