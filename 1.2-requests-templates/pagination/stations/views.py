from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings
import csv


def bus_stations(request):
    """
    View для отображения списка остановок с пагинацией
    """
    # Читаем все данные из CSV-файла
    stations_data = []

    # Путь к файлу берем из настроек
    csv_file_path = settings.BUS_STATION_CSV

    # Открываем файл и читаем данные
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Добавляем нужные поля в список
            stations_data.append({
                'Name': row.get('Name', ''),  # Название остановки
                'Street': row.get('Street', ''),  # Улица
                'District': row.get('District', ''),  # Район
                # Можно добавить и другие поля, если нужно
            })

    # Создаем пагинатор: по 10 элементов на странице
    paginator = Paginator(stations_data, 10)

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page', 1)

    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)

    # Формируем контекст для шаблона
    context = {
        'page_obj': page_obj,
        'bus_stations': page_obj.object_list,  # Список остановок на текущей странице
    }

    return render(request, 'stations/index.html', context)