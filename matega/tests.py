from django.test import TestCase
from .models import *
from django.utils import timezone
from django.test import Client


# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):
    #  time = timezone.now()
        self.notChef = User.objects.create(username="nilsen", password="pannekake12345")
        self.nils = User.objects.create(username="nilsen2", password="pannekake12345", first_name="Nils", last_name="Pettersen", is_chef=True)
        self.chef = Chef.objects.create(user=self.nils, workplace="Oslo", info="I am a chef")
        ingredient = Ingredient.objects.create(ingredient="Egg", ingredient_type="Egg")
        self.c = Client()

    def test_chef_fields(self):
        user_object = User.objects.get(first_name="Nils")
        self.assertEqual(user_object.is_chef, True)
        self.assertEqual(user_object.last_name, "Pettersen")
