from django.shortcuts import render
from .models import Article


def articles_list(request):
    template = 'articles/news.html'

    # Получаем статьи с оптимизацией запросов
    articles = Article.objects.prefetch_related('scopes__tag').order_by('-published_at')

    # Создаем новый атрибут для отсортированных scopes, не заменяя оригинальный
    for article in articles:
        # Получаем все связи
        scopes_list = list(article.scopes.all())
        # Сортируем: сначала основные, потом по имени тега
        scopes_list.sort(key=lambda x: (not x.is_main, x.tag.name))
        # Добавляем новый атрибут, не заменяя существующий scopes
        article.sorted_scopes = scopes_list

    context = {
        'object_list': articles,
    }

    return render(request, template, context)