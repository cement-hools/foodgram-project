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


class Tag(models.Model):
    TAG_COLOR = (
        ('tags__checkbox_style_orange', 'Оранжевый',),
        ('tags__checkbox_style_green', 'Зеленый'),
        ('tags__checkbox_style_purple', 'Фиолетовый'),
    )
    title = models.CharField('Название', max_length=50, null=True)
    color = models.CharField('Цвет', max_length=50, choices=TAG_COLOR)

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
    tags = models.ManyToManyField(Tag, related_name='recipes')
    title = models.CharField('название рецепта', max_length=256, blank=False)
    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='изображение',
        blank=True,
        null=True,
        default='default.jpg',
    )
    description = models.TextField('описание рецепта', blank=False)
    cooking_time = models.PositiveSmallIntegerField('время приготовления')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe_ingredient',
        through='IngredientAmount',
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
        Ingredient, on_delete=models.CASCADE, verbose_name='ингредиент',
        blank=False,
        related_name='amount',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients_amount',
        blank=False,
        verbose_name='рецепт',
    )
    amount = models.DecimalField('количество', max_digits=6, decimal_places=1,
                                 blank=False)

    class Meta:
        verbose_name = 'кол-во ингредиента'
        verbose_name_plural = 'кол-во ингредиентов'

    def __str__(self):
        ingredient = self.ingredient
        amount = self.amount
        dimension = ingredient.dimension
        return (f'{ingredient}: {amount}{dimension} - рецепт #{self.recipe.id}'
                f' {self.recipe}')


class FavoriteRecipe(models.Model):
    """Избранные рецепты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='at_favorites'
    )
    pub_date = models.DateTimeField(
        'дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-recipe__pub_date',)

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class Follow(models.Model):
    """Подписка на автора."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    pub_date = models.DateTimeField('дата добавления', auto_now_add=True)

    class Meta:
        unique_together = ("user", "author")
