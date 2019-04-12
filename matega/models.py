from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
import os
from .choices import *


def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)


class User(AbstractUser):
    is_chef = models.BooleanField(default=False)
    asked_for_perm = models.BooleanField(default=False)
    saved_recipes = models.ManyToManyField('Recipe', blank=True)

    def add_recipe_to_fav(self, recipe_id):
        for recipe_ in Recipe.objects.all():
            if recipe_.id == recipe_id:
                self.saved_recipes.add(recipe_id)
                print(self.saved_recipes.values_list())

    def remove_recipe_from_fav(self, recipe_id):
        for recipe_ in self.saved_recipes.values_list():
            if recipe_[0] == recipe_id:
                self.saved_recipes.remove(recipe_)
                print(self.saved_recipes.values_list())


class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_chef")
    workplace = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_image_path, blank=True, default="default_m.png")
    info = models.TextField()
    merit = models.CharField(max_length=75, default="")
    education = models.CharField(max_length=75, default="")

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=30)
    ingredient_type = models.CharField(max_length=30, choices=ingredient_choices)

    def __str__(self):
        return self.ingredient


class ValueIngredient(models.Model):
    value = models.CharField(max_length=30)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.value) + " " + self.ingredient.__str__()


class Recipe(models.Model):
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    ingredients = models.ManyToManyField(Ingredient)
    values = models.ManyToManyField(ValueIngredient)
    pub_date = models.DateTimeField('date published', null=True)
    recipe_text = models.TextField(null=True)
    num_stars = models.IntegerField(null=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, default="default_m.png")

    def __str__(self):
        return self.name

    def add_value_to_values(self, value):
        self.values.add(value)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_rating")
    rating = models.IntegerField(null=True)
