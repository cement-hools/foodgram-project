from django.contrib import admin

from .models import Ingredient, IngredientAmount, Recipe, Tag, FavoriteRecipe, \
    Follow


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInline,)


admin.site.register(Ingredient, )
admin.site.register(IngredientAmount, )
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(FavoriteRecipe)
admin.site.register(Follow)
