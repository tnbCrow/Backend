import factory
from factory.django import DjangoModelFactory

from v1.third_party.tnbCrow.constants import VERIFY_KEY_LENGTH

from ..models import User, Wallet


class UserFactory(DjangoModelFactory):
    email = factory.Faker('email')
    memo = factory.Faker('pystr', max_chars=44)
    loaded = factory.Faker('pyint')
    locked = factory.Faker('pyint')
    reputation = factory.Faker('pyint')
    username = factory.Faker('pystr', max_chars=150)

    class Meta:
        model = User


class WalletFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    account_number = factory.Faker('pystr', max_chars=VERIFY_KEY_LENGTH)
    is_primary = factory.Faker('pybool')

    class Meta:
        model = Wallet
