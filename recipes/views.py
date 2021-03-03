import csv

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from recipes.models import Ingredient, Recipe


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 2)  # показывать по 1 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {
        'range': range(7),
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'index.html', context)

def fill_tables(request):
    # заполняем категории
    with open('ingredients/ingredients.csv', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row[0] + '   ' + row[1])
            _, created = Ingredient.objects.get_or_create(
                title=row[0],
                dimension=row[1],
            )
            # print(_, created)
    return HttpResponse('ok')