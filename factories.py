# tests/factories.py

import factory
from faker import Faker
from myapp.models import Product  # Update this import to match your project structure

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    price = factory.LazyFunction(lambda: round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2))
    category = factory.LazyFunction(lambda: fake.random_element(elements=['Electronics', 'Books', 'Clothing', 'Home']))

