from django.shortcuts import render
from django.http import HttpResponse

# База данных рецептов
DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 300,
        'сыр, г': 50,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 0.5,
    },
}


def dish_view(request, dish_name):
    """
    View для отображения рецепта блюда
    """
    recipe = DATA.get(dish_name)

    if recipe is None:
        return HttpResponse(f"Рецепт для '{dish_name}' не найден", status=404)

    # Получаем параметр servings
    servings_param = request.GET.get('servings', '1')

    try:
        servings = int(servings_param)
        if servings <= 0:
            servings = 1
    except ValueError:
        servings = 1

    # Масштабируем рецепт
    scaled_recipe = {}
    for ingredient, amount in recipe.items():
        scaled_recipe[ingredient] = amount * servings

    # Формируем текстовый ответ
    response_lines = []
    for ingredient, amount in scaled_recipe.items():
        response_lines.append(f"{ingredient}: {amount}")

    return HttpResponse('\n'.join(response_lines), content_type='text/plain; charset=utf-8')