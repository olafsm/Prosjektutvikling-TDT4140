from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.index, name='index'),
    path('ingredient_search/', views.ingredient_search, name='ingredient_search'),
    path('signup/', views.signup, name="signup"),
    path('recipe/<recipe_id>', views.recipe, name='recipe'),
    path('my_recipes/<user_id>', views.my_recipes, name='my_recipes'),
    path('chef_site/<chef_id>', views.chef_site, name='chef_site'),
    path('my_site/<user_id>', views.chef_site_2, name='my_site'),
    path('add_recipe', views.add_recipe, name='add_recipe'),
    path('chef_edit', views.chef_edit, name='chef_edit'),
    path('authorize_chef/', views.authorize_chef, name='authorize_chef'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/add_recipe_to_user/$', views.add_recipe_to_user, name='add_recipe_to_user'),
    url(r'^ajax/remove_recipe_from_user/$', views.remove_recipe_from_user, name='remove_recipe_from_user'),
    url(r'^ajax/is_fav_recipe/$', views.is_fav_recipe, name='is_fav_recipe'),
    url(r'^ajax/add_rating/$', views.add_rating, name='add_rating'),
    url(r'^ajax/sort_by_ingredients/$', views.sort_by_ingredients, name='sort_by_ingredients'),
]
