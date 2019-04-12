from django.shortcuts import render, redirect
from datetime import datetime
from .models import Ingredient, Recipe, Chef, User, Rating
from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from matega.forms import ChefUserForm, UserForm, RecipeModelForm, AddIngredientForm, ChefEditForm, AddValueIngredient
from django.db.models import Avg
# Create your views here.


def is_chef(user):
    return user.is_authenticated and (user.is_chef or user.is_superuser)


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def get_chef_id(user):
    this_chef = get_object_or_404(Chef, user=user)
    return this_chef.id


def my_recipes(request, user_id):
    """
    :param request:
    :param user_id:
    Handles the requests from /my_recipes/

    **Context**

    All :model:`matega.recipe` that the user has saved and the users id.

    **Template:**

    :template:`my_recipes.html`
    """
    user = get_object_or_404(User, pk=user_id)
    recipes_all = []
    for r_ in user.saved_recipes.values_list():
        recipes_all.append(Recipe.objects.get(pk=r_[0]))
    recipes_filtered = []

    # Liste over ingredienser som er huket av pa nettsiden
    owned_ingredients = request.POST.getlist('ingredients')

    for r in recipes_all:
        ingredients = set()
        for ing in r.ingredients.all():
            ingredients.add(ing.ingredient.__str__())

        missing = len(list(ingredients - set(owned_ingredients)))
        recipes_filtered.append((r, missing))

    recipes_sorted = sorted(recipes_filtered, key=lambda x: x[1])

    recipes_final = []
    for r in recipes_sorted:
        recipes_final.append(r[0])
    context = {
        'saved_recipes': recipes_final,
        'user_id': int(user_id),
    }
    return render(request, 'my_recipes.html', context=context)


def sort_by_ingredients_match(request):
    """
    :param request:

    **Context**
    All :model:`matega.recipe` sorted by amount of missing ingredients

    **Template**
    :template:`my_recipes.html`
    """
    recipes_all = Recipe.objects.all()
    recipes_filtered = []

    # Liste over ingredienser som er huket av pa nettsiden
    owned_ingredients = request.POST.getlist('ingredients')

    for r in recipes_all:
        ingredients = set()
        for ing in r.ingredients.all():
            ingredients.add(ing.ingredient.__str__())

        missing = len(list(ingredients - set(owned_ingredients)))
        recipes_filtered.append((r, missing))

    recipes_sorted = sorted(recipes_filtered, key=lambda x: x[1])

    recipes_final = []
    for r in recipes_sorted:
        recipes_final.append(r[0])

    context = {
        'latest_recipe_list': recipes_final
    }
    return render(request, 'index.html', context)


def sort_by_ingredients(request):
    """
    Handles the requests from /ajax/sort_by_ingredients/

    **Data**

    Ids of all :model:`matega.recipe` in sorted order.
    """
    recipes_all = Recipe.objects.all()
    recipes_filtered = []

    # Liste over ingredienser som er huket av pa nettsiden
    owned = str(request.GET.get('ingredients'))
    owned_ingredients = owned[1:len(owned)-1].replace('"', "").split(",")

    for r in recipes_all:
        ingredients = set()
        for ing in r.ingredients.all():
            ingredients.add(ing.ingredient.__str__())
        missing = len(list(ingredients - set(owned_ingredients)))
        recipes_filtered.append((r, missing))

    recipes_sorted = sorted(recipes_filtered, key=lambda x: x[1])

    recipes_final = []
    for r in recipes_sorted:
        recipes_final.append(r[0].id)
    print(recipes_final)

    data = {
        'latest_recipe_list': recipes_final,
    }

    return JsonResponse(data)


def index(request):
    """

    :param request:

    Index page, handles requests from / and /index/

    **Context**

    All :model:`matega.recipe`

    **Template:**

    :template:`index.html`

    """
    recipes_all = Recipe.objects.all()
    context = {
        'latest_recipe_list': recipes_all,
    }
    return render(request, 'index.html', context=context)


def ingredient_search(request):
    """
    Handles the requests from /ingredient_search/

    **Context**

    All :model:`matega.ingredient` and their respective ingredient types.

    **Template:**

    :template:`ingredient_search.html`
    """
    ingredients_all = Ingredient.objects.all()

    if request.method == 'POST':
        return sort_by_ingredients_match(request)
    else:
        ingredient_types = {}

        for ing in ingredients_all:
            if ing.ingredient_type in ingredient_types.keys():
                ingredient_types[ing.ingredient_type].append(ing)
            else:
                ingredient_types[ing.ingredient_type] = [ing]

        context = {
            'ingredients': ingredients_all,
            'ingredient_types': ingredient_types,
        }
        return render(request, 'ingredient_search.html', context=context)


@user_passes_test(is_admin, 'login')
def authorize_chef(request):
    """
    :param request:
    Handles requests from /authorize_chef/.
    Approves requests to become a chef
    **Context**

    All :model:`matega.Chef` where Chef.user.asked_for_perm = True

    **Template**

    :template:`authorize_chef.html`
    """
    chefs = Chef.objects.filter(user__asked_for_perm=True)
    print(chefs)
    if request.method == 'POST':
        print(request.POST)

        chef_user = request.POST.get("chef.id")
        chef = get_object_or_404(Chef, pk=chef_user)
        print(chef)

        chef.user.is_chef = True
        chef.user.asked_for_perm = False
        chef.user.save()
        messages.add_message(request, messages.INFO, 'Kokken er nå godkjent!')

        return redirect('authorize_chef')

    context = {
        'chefs': chefs,
    }
    return render(request, 'authorize_chef.html', context=context)


def signup(request):
    """
    :param request:
    Handles registration of users and chefs.
    **Context**
    Forms for entering user details

    **template**
    :template:`registration/signup.html
    :return:
    """
    chef_form = ChefUserForm(auto_id='chef_%s')
    user_form = UserCreationForm()

    if request.method == 'POST' and "brukerreg" in request.POST:
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('index')

    if request.method == 'POST' and "kokkereg" in request.POST:
        chef_form = ChefUserForm(request.POST, request.FILES or None)
        if chef_form.is_valid():
            chef_user = chef_form.save(commit=False)
            chef_user.asked_for_perm = True
            chef_user.save()
            chef = Chef.objects.create(
                    user=chef_user,
                    workplace=chef_form.cleaned_data['workplace'],
                    info=chef_form.cleaned_data['info'],
                    image=chef_form.cleaned_data['image'],
                    merit=chef_form.cleaned_data['merit'],
                    education=chef_form.cleaned_data['education'])
            chef.save()
            login(request, chef_user)
            return redirect('index')

    context = {
        'chef_form': chef_form,
        'user_form': user_form,
    }
    return render(request, 'registration/signup.html', context=context)


def validate_username(request):
    """
    :param request:
    Checks if a username is valid

    **Data**
    bool is_taken
    :return:
    """
    username = request.GET.get('username', None)

    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def is_fav_recipe(request):
    """
    Handles the requests from /ajax/is_fav_recipe/
    Checks if a :model:`matega.recipe` is a saved recipe for a :model:'matega.user'

    **Data**
    Boolean if :model:`matega.recipe` is a saved recipe for :model:'matega.user'
    """
    user_id = int(request.GET.get('user_id', None))
    recipe_id = int(request.GET.get('recipe_id', None))
    is_fav = False

    user = User.objects.get(pk=user_id)

    for rec in user.saved_recipes.values_list():
        if rec[0] == recipe_id:
            is_fav = True

    data = {
        'is_fav': is_fav
    }
    return JsonResponse(data)


def add_recipe_to_user(request):
    """
    Handles the requests from /ajax/add_recipe_to_user/
    Adds a :model:`matega.recipe` to saved_recipes for a :model:'matega.user'

    **Data**
    None
    """
    user_id = int(request.GET.get('user_id', None))
    recipe_id = int(request.GET.get('recipe_id', None))

    user = User.objects.get(pk=user_id)
    user.add_recipe_to_fav(recipe_id)

    data = {}
    return JsonResponse(data)


def add_rating(request):
    """
    :param request:
    Handles requests from /ajax/add_rating

    Adds a new rating to a specified recipe
    :return:
    """
    recipe_id = int(request.GET.get('recipe'))
    rating = int(request.GET.get('rating'))
    recipe2 = Recipe.objects.get(pk=recipe_id)
    try:
        rating_object = Rating.objects.get(recipe=recipe2, user=request.user)
    except Rating.DoesNotExist:
        rating_object = None

    if not rating_object:
        Rating.objects.create(
            recipe=recipe2,
            user=request.user,
            rating=rating
        )
    else:
        rating_object.rating = rating
        rating_object.save()

    data = {}
    return JsonResponse(data)


def remove_recipe_from_user(request):
    """
    Handles the requests from /ajax/remove_recipe_from_user/
    Removes a :model:`matega.recipe` from saved_recipes for a :model:'matega.user'

    **Data**
    None
    """
    user_id = int(request.GET.get('user_id', None))
    recipe_id = int(request.GET.get('recipe_id', None))

    user = User.objects.get(pk=user_id)
    user.remove_recipe_from_fav(recipe_id)

    data = {}
    return JsonResponse(data)


def recipe(request, recipe_id):
    """
    Handles the requests from /recipe/<recipe_id>/

    **Context**

    The :model:`matega.recipe` with recipe.id equal to <recipe_id> and its average rating.

    **Template:**

    :template:`recipe.html`
    """
    recipe_ = get_object_or_404(Recipe, pk=recipe_id)
    rating = Rating.objects.filter(recipe_id=recipe_id).aggregate(average_rating=Avg('rating'))

    context = {
        'avg_rating': rating['average_rating'],
        'recipe': recipe_
    }
    return render(request, 'recipe.html', context=context)


def chef_site(request, chef_id):
    """
    Handles the requests to go to a given chef's site with the chef's recipes.

    **Context**

    The :model:`matega.chef` with chef.id equal to <chef_id> and its average rating.
    The :model:`matega.recipe` with recipe.chef.id equal to <chef_id>.

    **Template:**

    :template:`chef_site.html`
    """
    chef = get_object_or_404(Chef, pk=chef_id)
    recipe_list = Recipe.objects.filter(chef__id__contains=chef_id)
    return render(request, "chef_site.html", {'chef': chef, 'recipes': recipe_list})


def chef_site_2(request, user_id):
    """
    Handles the requests to go to your own chefsite with info about you and your recipes.

    **Context**

    The :model:`matega.chef` with chef.id equal to <chef_id> and its average rating.
    The :model:`matega.recipe` with recipe.chef.id equal to <chef_id>.

    **Template:**

    :template:`chef_site.html`
    """
    user = get_object_or_404(User, pk=user_id)

    chef = get_object_or_404(Chef, user=user)
    recipe_list = Recipe.objects.filter(chef__id__contains=chef.id)
    return render(request, "chef_site.html", {'chef': chef, 'recipes': recipe_list})


@user_passes_test(is_chef, 'login/')
def chef_edit(request):
    """
    Handles the requests to go to subsite to edit chefinfo.

    **Context**
    ChefEditForm, saves user info for the currently logged in chef.

    **Template:**

    :template:`chef_edit.html`
    """
    # felt i chefuserform: workplace, info, image, education, merit, first_name_last_name, username
    # get kokken og endre kokken sine egne forms
    # initial_data = {
    #
    #   }
    #  edit_form = ChefUserForm(request.POST or None)
    #
    #   if request.method == 'POST' and 'edit_form' in request.POST:
    #

    chef_form = ChefEditForm(request.POST or None, request.FILES or None, instance=request.user.user_chef)

    if request.method == 'POST':
        if chef_form.is_valid():
            chef_form.save()
            return redirect('index')

    context = {
        'chef_form': chef_form
    }
    return render(request, "chef_edit.html", context=context)


@user_passes_test(is_chef, 'login/')
def add_recipe(request):
    """
    Handles the requests from /add_recipe/.

    **Context**
    AddIngredientForm - form for adding new ingredients
    RecipeModelForm - form for adding new recipes

    **Template:**

    :template:`add_recipe.html` and :template:`add_values.html`
    """
    initial_data = {
        'pub_date': datetime.now(),
        'chef': Chef.objects.get(user=request.user)
    }
    ingredient_form = AddIngredientForm(request.POST or None)
    recipe_form = RecipeModelForm(request.POST or None, request.FILES or None, initial=initial_data)
    value_form = AddValueIngredient(request.POST or None)

    if request.method == 'POST' and 'value' in request.POST:
        if value_form.is_valid():
            v = value_form.save(commit=False)
            pk = request.POST['ingredient']
            v.ingredient = Ingredient.objects.get(pk=pk)
            v.save()
            rpk = request.POST['recipe']
            rec = Recipe.objects.get(pk=rpk)
            rec.add_value_to_values(v)
            return

    elif request.method == 'POST' and 'recipe_form' in request.POST:
        if recipe_form.is_valid():
            r = recipe_form.save(commit=False)
            r.chef = Chef.objects.get(user=request.user)
            r.save()
            recipe_form.save_m2m()
            rec = recipe_form.instance

            forms = []
            for i in range(0, len(rec.ingredients.values())):
                forms.append(AddValueIngredient)

            context = {
                'forms': forms,
                'recipe': rec,
                'ingredients': rec.ingredients.values(),
                'length': (len(forms)),
            }

            return render(request, 'add_values.html', context)

    elif request.method == 'POST' and 'ingredient_form' in request.POST:
        if ingredient_form.is_valid():
            ingredient_form.save()
            return redirect('add_recipe')
    context = {
        'ingredient_form': ingredient_form,
        'form': recipe_form
    }
    return render(request, 'add_recipe.html', context=context)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, 'Du er nå utlogget!')
