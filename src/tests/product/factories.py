import decimal
import random
from random import choice

import factory

from faker import Faker

from src.product.models import Category, Product


fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda obj: fake.name())


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda obj: fake.numerify(text=choice(["AMD Ryzen % %%##X", "Intel Core i%-%%##K"])))
    small_description = factory.LazyAttribute(lambda obj: fake.text())
    price = factory.LazyAttribute(lambda obj: decimal.Decimal(fake.random_int(min=100, max=10000, step=50)))
    available = factory.LazyAttribute(lambda obj: random.choice([True, False]))
