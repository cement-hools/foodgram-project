from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=50)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
    )
    title = models.CharField('название рецепта', max_length=256, blank=False)
    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='изображение',
    )
    text = models.TextField('описание рецепта', blank=False)
    cooking_time = models.PositiveSmallIntegerField('время приготовления')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredient',
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='ингредиент',
    )
    pub_date = models.DateTimeField(
        'дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    """Количество ингредиента в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients_amount',
        verbose_name='рецепт',
    )
    amount = models.DecimalField('количество', max_digits=6, decimal_places=1)

    class Meta:
        verbose_name = 'кол-во ингредиента'
        verbose_name_plural = 'кол-во ингредиентов'

    def __str__(self):
        ingredient = self.ingredient
        amount = self.amount
        dimension = ingredient.dimension
        return (f'{ingredient}: {amount}{dimension} - рецепт #{self.recipe.id}' 
               f' {self.recipe}')
