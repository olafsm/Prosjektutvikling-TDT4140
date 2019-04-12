from django.contrib import admin
from . import models

# Registrering av modeller for innebygd django-admin.
admin.site.register(models.ValueIngredient)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.Chef)
admin.site.register(models.User)
admin.site.register(models.Rating)
