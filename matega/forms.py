from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Recipe, Ingredient, Chef, ValueIngredient
from .choices import *


# Registrering av kokk
class ChefUserForm(UserCreationForm):
    workplace = forms.CharField(max_length=254)
    info = forms.CharField(widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "3", }))
    image = forms.ImageField(required=False)
    education = forms.CharField(max_length=75)
    merit = forms.CharField(max_length=75)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')


# Endring av kokkeinformasjon
class ChefEditForm(forms.ModelForm):
    workplace = forms.CharField(max_length=254, required=True)
    info = forms.CharField(required=True, max_length=1500, widget=forms.Textarea(
        attrs={'width': "100%", 'cols': "80", 'rows': "3", }))
    image = forms.ImageField(required=True)
    education = forms.CharField(max_length=75, required=True)
    merit = forms.CharField(max_length=75, required=True)

    class Meta:
        model = Chef
        fields = ['workplace', 'info', 'image', 'education', 'merit']


# Bruker registrering
class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


# Registrering av ingredienser
class AddIngredientForm(forms.ModelForm):
    ingredient = forms.CharField(required=True, label='Ingrediens', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrediens: Eks. melk, hvete, entrecote'
        }
    ))
    ingredient_type = forms.ChoiceField(required=True, label='Velg kategori',
                                        initial='Velg kategori', choices=ingredient_choices)

    class Meta:
        model = Ingredient
        fields = ['ingredient', 'ingredient_type']


# Registrering av oppskrifter
class RecipeModelForm(forms.ModelForm):
    name = forms.CharField(label='Oppskriftsnavn', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Skriv inn oppskriftsnavn'
        }
    ))
    pub_date = forms.DateTimeField(
        required=False,
        label='Publiseringsdato',
        widget=forms.DateInput(
            format='%m/%d/%Y %H:%M',
            attrs={
                'class': 'form-control',
                'readonly': 'True'
            }
        ))
    recipe_text = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Skriv inn fremgangsmåte & info'
        }
    ))
    num_stars = forms.IntegerField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'readonly': 'True',
            'placeholder': 'Du kan ikke sette stjernekast på egen oppskrift'
        }
    ))

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'pub_date', 'recipe_text', 'num_stars', 'image']


# Registrering av ingredienser med en spesifikk verdi
class AddValueIngredient(forms.ModelForm):
    value = forms.CharField(label='Ingrediensverdi', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Skriv inn mengde'
        }
    ))

    class Meta:
        model = ValueIngredient
        fields = ['value']
