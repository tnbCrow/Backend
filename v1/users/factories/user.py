import factory
from factory.django import DjangoModelFactory

from v1.third_party.tnbCrow.constants import MAX_POINT_VALUE
from ..models import User


class UserFactory(DjangoModelFactory):
    email = factory.Faker('email')
    memo = factory.Faker('pystr', max_chars=44)
    balance = factory.Faker('pyint', max_value=MAX_POINT_VALUE)
    reputation = factory.Faker('pyint')
    username = factory.Faker('pystr', max_chars=150)

    class Meta:
        model = User
