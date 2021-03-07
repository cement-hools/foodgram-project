from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.del_recipe, name='del_recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path(
        'recipe/<int:recipe_id>/favorite/add/',
        views.add_recipe_in_favorite,
        name='favorite_add',
    ),
    path(
        'recipe/<int:recipe_id>/favorite/del/',
        views.del_recipe_in_favorite,
        name='favorite_del',
    ),
    path(
        'recipes/<str:username>/',
        views.authors_recipes,
        name='authors_recipes'
    ),
    path('follow/<str:username>/', views.author_follow, name='follow',),
    path('unfollow/<str:username>/', views.author_unfollow, name='unfollow',),
    path('subscriptions/', views.subscriptions, name='subscriptions', ),

    path('add_recipe/', views.add_recipe, name='add_recipe'),

    path('fill/', views.fill_tables),
]
