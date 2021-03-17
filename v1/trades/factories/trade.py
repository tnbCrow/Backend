import factory
from factory.django import DjangoModelFactory

from v1.users.factories.user import UserFactory
from v1.constants.factories.constants import TransactionTypeFactory, CurrencyFactory, PaymentMethodFactory, ExchangeFactory

from ..models import TradePost


class TradePostFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    owner_role = factory.Faker('pyint')
    transaction_type = factory.SubFactory(TransactionTypeFactory)
    currency = factory.SubFactory(CurrencyFactory)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    exchange = factory.SubFactory(ExchangeFactory)
    margin = factory.Faker('pyint')
    rate = factory.Faker('pyint')
    amount = factory.Faker('pyint')
    terms_of_trade = factory.Faker('text')
    min_reputation = factory.Faker('pyint')
    broadcast_trade = factory.Faker('pybool')
    is_active = factory.Faker('pybool')

    class Meta:
        model = TradePost
