import factory
from factory.django import DjangoModelFactory

from ..models import Exchange, TransactionType, PaymentMethod, Currency, TransactionFee, Country


class ExchangeFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=250)
    price = factory.Faker('pyint')

    class Meta:
        model = Exchange


class TransactionTypeFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = TransactionType


class PaymentMethodFactory(DjangoModelFactory):
    type = factory.SubFactory(TransactionTypeFactory)
    name = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = PaymentMethod


class CurrencyFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)

    class Meta:
        model = Currency


class TransactionFeeFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)
    charge = factory.Faker('pyint')

    class Meta:
        model = TransactionFee


class CountryFactory(DjangoModelFactory):
    name = factory.Faker('pystr', max_chars=255)
    alpha_two_code = factory.Faker('pystr', max_chars=2)
    alpha_three_code = factory.Faker('pystr', max_chars=3)
    phone_code = factory.Faker('pystr', max_chars=6)

    class Meta:
        model = Country
