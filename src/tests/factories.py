import factory

from faker import Faker

# from product.models import Category


fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.Category"

    name = fake.name()[:20]
