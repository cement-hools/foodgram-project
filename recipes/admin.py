from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe

admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Recipe)