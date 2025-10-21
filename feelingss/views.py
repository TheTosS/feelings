
from django.shortcuts import render, get_object_or_404
from .models import Feeling
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, FeelingForm
from .models import Feeling
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


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
        form = FeelingForm(request.POST)
        if form.is_valid():
            feeling = form.save(commit=False)
            feeling.user = request.user
            feeling.save()
            messages.success(request, 'Запись добавлена!')
            return redirect('home')
    else:
        form = FeelingForm()

    return render(request, 'index.html', {
        'feelings': feelings,
        'form': form
    })


# Защищенные представления
@login_required
def profile(request):
    return render(request, 'registration/login.html')


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
