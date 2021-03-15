import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('dimension', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(
                    validators=[django.core.validators.MinValueValidator(1)],
                    verbose_name='количество')),
                ('ingredient',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='recipes_amount',
                                   to='recipes.Ingredient',
                                   verbose_name='ингредиент')),
            ],
            options={
                'verbose_name': 'Кол-во ингредиента',
                'verbose_name_plural': 'Кол-во ингредиентов',
                'ordering': ('-recipe__pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256,
                                           verbose_name='название рецепта')),
                ('image', models.ImageField(blank=True, default='default.jpg',
                                            null=True,
                                            upload_to='recipe_images/',
                                            verbose_name='изображение')),
                ('description',
                 models.TextField(verbose_name='описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(
                    verbose_name='время приготовления')),
                ('pub_date',
                 models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='дата публикации')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='recipes',
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='автор рецепта')),
                ('ingredients', models.ManyToManyField(related_name='recipes',
                                                       through='recipes.IngredientAmount',
                                                       to='recipes.Ingredient',
                                                       verbose_name='ингредиент')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True,
                                           verbose_name='Название')),
                ('color', models.CharField(
                    choices=[('tags__checkbox_style_orange', 'Оранжевый'),
                             ('tags__checkbox_style_green', 'Зеленый'),
                             ('tags__checkbox_style_purple', 'Фиолетовый')],
                    max_length=50, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('pub_date',
                 models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='дата добавления')),
                ('recipe',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='at_shopping_lists',
                                   to='recipes.Recipe')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='users_shopping_lists',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes',
                                         to='recipes.Tag'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ingredients_amount', to='recipes.Recipe',
                verbose_name='рецепт'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True,
                                                  verbose_name='дата добавления')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='following',
                                   to=settings.AUTH_USER_MODEL)),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='follower',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('pub_date',
                 models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='дата добавления')),
                ('recipe',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='at_favorites',
                                   to='recipes.Recipe')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='favorite_recipes',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ('-recipe__pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'),
                                               name='unique_following'),
        ),
    ]
