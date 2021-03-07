import csv

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from foodgram import settings
from .forms import RecipeForm
from .models import Ingredient, Recipe, FavoriteRecipe, Follow

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
            # print(_, created)
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
    # amount, created = IngredientAmount.objects.get_or_create(
    #     ingredient=ingredient,
    #     recipe=recipe,
    #     amount=25,
    # )

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


def index(request):
    """Главная страница. Список всех рецептов."""
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'range': range(7),
        'page': page,
        'paginator': paginator,
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
    recipe_list = Recipe.objects.filter(author__username=username)
    paginator = Paginator(recipe_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'username': username,
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
        print(form.cleaned_data)
        print(form.cleaned_data['tags'])
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect(to=view_recipe, recipe_id=recipe.id)
    print(form.errors.as_data())
    tags = []
    context = {
        'form': form,
        'tags': tags,
    }
    return render(request, 'recipe_form.html', context)


@login_required
def edit_recipe(request, recipe_id):
    """Редактировать рецепт."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect(to=view_recipe, recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect(to=view_recipe, recipe_id=recipe_id)
    print(form.errors.as_data())
    context = {
        'form': form,
        'recipe': recipe,
    }
    return render(request, 'recipe_form.html', context)


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
    my_user = request.user
    recipes_list = my_user.favorite_recipes.all()
    paginator = Paginator(recipes_list, OBJECT_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
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
