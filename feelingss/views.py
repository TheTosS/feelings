from . import forms
from .forms import CustomUserCreationForm, FeelingForm
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

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


def feelings_wiki(request):
    feelings1 = Feeling.objects.all()  # Запрашиваем все чувства из базы данных
    return render(request, 'feelings_wiki.html', {'feelings': feelings1})



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


def chat(request):
    """Страница чата"""
    return render(request, 'chat.html')


@csrf_exempt
def chat_send(request):
    """API endpoint для отправки сообщений в чат"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower()

            # Простые ответы бота на основе ключевых слов
            bot_responses = {
                'default': [
                    "Расскажите подробнее о том, что вы чувствуете.",
                    "Понимаю. Как это ощущение влияет на вашу повседневную жизнь?",
                    "Спасибо, что делитесь. Что, по вашему мнению, вызывает эти эмоции?",
                ],
                'привет': [
                    "Здравствуйте! Как вы себя чувствуете сегодня?",
                    "Привет! Расскажите, что у вас на душе.",
                ],
                'груст': [
                    "Мне жаль, что вы чувствуете грусть. 🫂 Хотите рассказать, что произошло?",
                    "Грусть показывает, что что-то было для вас важно. Давайте разберемся.",
                ],
                'счастлив': [
                    "Это замечательно! 😊 Что именно вызывает у вас это чувство?",
                    "Радость - прекрасная эмоция! Поделитесь своим счастьем!",
                ]
            }

            # Поиск подходящего ответа
            response = None
            for keyword, responses in bot_responses.items():
                if keyword in user_message and keyword != 'default':
                    response = random.choice(responses)
                    break

            if not response:
                response = random.choice(bot_responses['default'])

            return JsonResponse({
                'success': True,
                'bot_response': response
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

    return JsonResponse({'success': False, 'error': 'Invalid method'})