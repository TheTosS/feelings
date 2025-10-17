
from django.shortcuts import render, get_object_or_404
from .models import Feeling



def index(request):
    return render(request, 'index.html')


def feelings(request):
    return render(request, 'feelings.html')


def description(request):
    return render(request, 'description.html')


def feelings_list(request):
    feelings = Feeling.objects.all()  # Получаем все чувства из базы
    return render(request, 'feelings_list.html', {'feelings': feelings})


def feeling_detail(request, feeling_id):
    feeling = get_object_or_404(Feeling, id=feeling_id)  # Получаем чувство по id (или 404)
    return render(request, 'feeling_detail.html', {'feeling': feeling})
