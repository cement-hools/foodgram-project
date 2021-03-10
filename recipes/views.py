import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from foodgram import settings
from .forms import RecipeForm
from .logic import get_ingredients, add_ingredients_to_recipe, save_recipe, \
    get_tags_for_filter
from .models import Ingredient, Recipe, FavoriteRecipe, Follow, ShoppingList

User = get_user_model()

OBJECT_PER_PAGE = settings.OBJECT_PER_PAGE


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
    return HttpResponse('ok')


def test(request):
    ingredient = Ingredient.objects.get(id=1)
    ingredient2 = Ingredient.objects.get(id=2)
    print(ingredient)
    recipe, _ = Recipe.objects.get_or_create(
        title='Пюре',
        author=request.user,
        description='xczv',
        cooking_time='3',
    )
    print(recipe, recipe.ingredients.all())
    recipe.ingredients.add(ingredient2,
                           through_defaults={'amount': 100}
                           )
    recipe.ingredients.create(
        through_defaults={
            'amount': 20,
            'ingredient': ingredient,
        }
    )

    for i in recipe.ingredients.all():
        print(i.amount.all())
    return HttpResponse()


@require_http_methods(['GET'])
def ingredients(request):
    """Вывод ингредиентов в форме"""
    if request.GET:
        query = (request.GET['query']).lower()
        ingredients_list = Ingredient.objects.values('title',
                                                     'dimension').filter(
            title__icontains=query)
        context = list(ingredients_list)
        return JsonResponse(context, safe=False)


def index(request):
    """Главная страница. Список всех рецептов."""
    tags, tags_for_filter = get_tags_for_filter(request)
    recipes = Recipe.objects.filter(tags__in=tags_for_filter)
    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'tags_for_filter': tags_for_filter,
    }
    return render(request, 'index.html', context)


def view_recipe(request, recipe_id):
    """Просмотр одного рецепта."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipe_view.html', context)


def authors_recipes(request, username):
    """Список рецептов одного автора."""
    tags, tags_for_filter = get_tags_for_filter(request)
    recipe_list = Recipe.objects.filter(author__username=username,
                                        tags__in=tags_for_filter)
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'username': username,
        'tags': tags,
        'tags_for_filter': tags_for_filter,
    }
    if request.user.is_authenticated:
        author = get_object_or_404(User, username=username)
        my_user = request.user
        follow = Follow.objects.filter(user=my_user, author__username=username)
        follow_or_author = follow or my_user == author
        print(follow_or_author)
        context['follow_or_author'] = follow_or_author
    print(context)
    return render(request, 'authors_recipes.html', context)


@login_required
def add_recipe(request):
    """Создание нового рецепта."""
    form = RecipeForm(request.POST or None, files=request.FILES or None, )
    print(request.POST)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect(to=view_recipe, recipe_id=recipe.id)
    print(form.errors.as_data())
    context = {
        'form': form,
    }
    return render(request, 'recipe_form.html', context)


@login_required
def edit_recipe(request, recipe_id):
    """Редактировать рецепт."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author and not request.user.is_staff:
        return redirect(to=view_recipe, recipe_id=recipe_id)

    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        recipe.ingredients.clear()
        form.save()
        ingredients = get_ingredients(request)
        print('ingredients', ingredients, recipe.id)
        add_ingredients_to_recipe(ingredients, recipe)
        return redirect(to=view_recipe, recipe_id=recipe_id)
    print(form.errors.as_data())
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe_edit_form.html', context)


@login_required
def del_recipe(request, recipe_id):
    """Удалить рецепт."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect(to=view_recipe, recipe_id=recipe_id)
    recipe.delete()
    return redirect(to=index)


@login_required
def favorite(request):
    """Все избранные рецепты."""
    tags, tags_for_filter = get_tags_for_filter(request)
    my_user = request.user
    recipes_list = my_user.favorite_recipes.filter(
        recipe__tags__in=tags_for_filter)
    paginator = Paginator(recipes_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'tags': tags,
        'tags_for_filter': tags_for_filter,
    }
    return render(request, 'favorite.html', context)


@login_required
def add_recipe_in_favorite(request, recipe_id):
    """Добавить рецепт в избранное."""
    my_user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _, created = FavoriteRecipe.objects.get_or_create(user=my_user,
                                                      recipe=recipe)
    print(created)
    # return redirect(to=view_recipe, recipe_id=recipe_id)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_recipe_in_favorite(request, recipe_id):
    """Удалить рецепт из избранного."""
    my_user = request.user
    favorite_recipe = get_object_or_404(FavoriteRecipe, user=my_user,
                                        recipe__id=recipe_id)
    favorite_recipe.delete()
    print('deleted', favorite_recipe)
    # return redirect(to=view_recipe, recipe_id=recipe_id)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def author_follow(request, username):
    """Подписаться на автора."""
    my_user = request.user
    my_author = get_object_or_404(User, username=username)
    if my_user == my_author:
        print('You are author!!!')
        return redirect(request.META.get('HTTP_REFERER'))
    _, created = Follow.objects.get_or_create(user=my_user, author=my_author)
    print('You are follow!!!', created)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def author_unfollow(request, username):
    """Убрать автора из подписок."""
    my_user = request.user
    my_author = get_object_or_404(User, username=username)
    authors = Follow.objects.filter(user=my_user, author=my_author)
    if authors.exists():
        authors.delete()
    # return redirect(to='authors_recipes', username=username)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def subscriptions(request):
    """Страница из рецептов избранных авторов"""
    my_user = request.user
    following_authors = User.objects.filter(following__user=my_user)
    paginator = Paginator(following_authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator
    }
    return render(request, 'subscriptions.html', context)


@require_http_methods(['GET'])
def purchases_list(request):
    print('GET DICK')
    context = {'success': True}
    return JsonResponse(context)


@require_http_methods(['POST', 'DELETE'])
def purchases(request, recipe_id):
    """Добавить/удалить в список покупок"""
    my_user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {'success': True}
    if request.method == 'POST':
        print('purchases POST')
        _, created = ShoppingList.objects.get_or_create(user=my_user,
                                                        recipe=recipe)
        return JsonResponse(context)
        context = {'success': True}
        return JsonResponse(context)
    print('purchases DELETE')
    favorite_recipe = get_object_or_404(ShoppingList, user=my_user,
                                        recipe=recipe)
    favorite_recipe.delete()
    return JsonResponse(context)


def shopping_list(request):
    """Страница Список покупок."""
    my_user = request.user
    shopping_list = my_user.users_shopping_lists.all
    context = {
        'shopping_list': shopping_list,
    }
    return render(request, 'shopping_list.html', context)


def shopping_list_save(request):
    """Скачать список ингредиентов"""
    my_user = request.user
    ingredient_list = Recipe.objects.prefetch_related(
        'ingredients', 'ingredients_amount'
    ).filter(
        shopping_lists__user=my_user
    ).order_by(
        'ingredients__title'
    ).values(
        'ingredients__title', 'ingredients__dimension'
    ).annotate(
        title=F('ingredients__title'),
        amount=Sum('ingredients_amount__amount'),
        dimension=F('ingredients__dimension')
    )
    ingredient_txt = []
    count = 1
    for item in ingredient_list:
        ingredient_txt.append(
            (f"{count}. {item['title'].capitalize()} "
             f"\u2014 {item['amount']} {item['dimension']}.\n")
        )
        count += 1

    filename = 'shoppinglist.txt'
    response = HttpResponse(ingredient_txt, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


@require_http_methods(['POST', 'DELETE'])
def favorites(request, recipe_id):
    """Добавить/удалить рецепт в избранное."""
    my_user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {'success': True}

    if request.method == 'POST':
        print('favorites POST')
        _, created = FavoriteRecipe.objects.get_or_create(user=my_user,
                                                          recipe=recipe)
        return JsonResponse(context)
    print('favorites DELETE')
    favorite_recipe = get_object_or_404(FavoriteRecipe, user=my_user,
                                        recipe__id=recipe_id)
    favorite_recipe.delete()
    return JsonResponse(context)
