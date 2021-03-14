from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=50)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Модель тега."""
    ORANGE = 'tags__checkbox_style_orange'
    GREEN = 'tags__checkbox_style_green'
    PURPLE = 'tags__checkbox_style_purple'
    TAG_COLOR = (
        (ORANGE, 'Оранжевый',),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
    )
    title = models.CharField('Название', max_length=50, null=True)
    color = models.CharField('Цвет', max_length=50, choices=TAG_COLOR)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
    amount = models.IntegerField(
        'количество',
        blank=False,
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'кол-во ингредиента'
        verbose_name_plural = 'кол-во ингредиентов'

    def __str__(self):
        ingredient = self.ingredient.title
        amount = self.amount
        dimension = ingredient.dimension
        recipe = self.recipe
        return (f'{ingredient}: {amount}{dimension} - рецепт #{recipe.id}'
                f' {recipe.title}')


class FavoriteRecipe(models.Model):
    """Избранный рецепт."""
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
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        user_username = self.user.username
        recipe = self.recipe.title
        return f'{user_username} добавил в избранное {recipe}'


class ShoppingList(models.Model):
    """Список покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_shopping_lists'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_lists'
    )
    pub_date = models.DateTimeField(
        'дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        user_username = self.user.username
        recipe = self.recipe.title
        return f'{user_username} добавил в список покупок {recipe}'


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
        unique_together = ('user', 'author',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        user_username = self.user.username
        author_username = self.author.username
        return f'{user_username} подписался на {author_username}'
