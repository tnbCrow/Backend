import factory
from factory.django import DjangoModelFactory

from v1.users.factories.user import UserFactory
from v1.constants.factories.constants import TransactionTypeFactory, CurrencyFactory, PaymentMethodFactory, ExchangeFactory

from ..models import TradePost, TradeRequest, ActiveTrade, CompletedTrade


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


class TradeRequestFactory(DjangoModelFactory):
    post = factory.SubFactory(TradePostFactory)
    initiator = factory.SubFactory(UserFactory)
    status = factory.Faker('pyint')
    message = factory.Faker('pystr', max_chars=255)
    amount = factory.Faker('pyint')

    class Meta:
        model = TradeRequest


class ActiveTradeFactory(DjangoModelFactory):
    post = factory.SubFactory(TradePostFactory)
    initiator = factory.SubFactory(UserFactory)
    initiator_confirmed = factory.Faker('pybool')
    owner_confirmed = factory.Faker('pybool')

    class Meta:
        model = ActiveTrade


class CompletedTradeFactory(DjangoModelFactory):
    seller = factory.SubFactory(UserFactory)
    buyer = factory.SubFactory(UserFactory)
    amount = factory.Faker('pyint')

    class Meta:
        model = CompletedTrade
