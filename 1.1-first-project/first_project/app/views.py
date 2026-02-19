from django.http import HttpResponse
from django.shortcuts import render, reverse
import os
from datetime import datetime


def home_view(request):
    """
    Домашняя страница со списком доступных страниц.
    """
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    """
    Возвращает текущее время в текстовом формате.
    """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    """
    Возвращает список файлов в рабочей директории в текстовом формате.
    """
    try:
        files_list = os.listdir('.')
        files_output = '\n'.join(files_list)
        msg = f'Содержимое рабочей директории:\n{files_output}'
    except Exception as e:
        msg = f'Ошибка при получении списка файлов: {e}'

    return HttpResponse(msg)