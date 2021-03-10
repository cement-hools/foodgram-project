from django.core.exceptions import NON_FIELD_ERRORS

from .models import IngredientAmount, Ingredient, Tag


def get_ingredients(request):
    """Взять ингредиенты из POST запроса."""
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_id = key.split('_')[-1]
            ingredient_name = request.POST[key]
            ingredient_value = int(request.POST[
                                       'valueIngredient_' + ingredient_id])

            ingredients[ingredient_name] = (
                    ingredients.get(ingredient_name, 0) + ingredient_value)
    return ingredients


def add_ingredients_to_recipe(ingredients, recipe):
    """Добавить ингредиенты в рецепт."""
    for title, amount in ingredients.items():
        ingredient = Ingredient.objects.get(title=title)
        ingredient_amount = IngredientAmount(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
        ingredient_amount.save()
    return True


def save_recipe(request, form):
    """Сохранить рецепт рецепт."""
    tags = form.cleaned_data['tags']
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    recipe.tags.set(tags)
    ingredients = get_ingredients(request)
    add_ingredients_to_recipe(ingredients, recipe)
    return recipe


def get_tags_for_filter(request):
    tags = Tag.objects.all()
    tags_id = [tag.id for tag in tags]
    request_teg_id = [int(tag_id) for tag_id in request.GET.getlist('tags')]
    tags_for_filter = request_teg_id or tags_id
    return tags, tags_for_filter,
