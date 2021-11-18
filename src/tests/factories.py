from random import choice

import factory

from faker import Faker

from src.product.models import Category, Product


fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = fake.name()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda obj: fake.numerify(text=choice("AMD Ryzen % %%##X", "Intel Core i%-%%##K")))
    small_description = factory.LazyAttribute(lambda obj: fake.text())
    price = factory.LazyAttribute(lambda obj: fake.random_int(min=100, max=1000, step=50))
    available = factory.LazyAttribute(lambda obj: fake.boolean())
