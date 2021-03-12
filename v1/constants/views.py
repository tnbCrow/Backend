from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

from .models import Country, TransactionType, Exchange, Currency
from .serializers import CountrySerializer, TransactionTypeSerializer, ExchangeSerializer, CurrencySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TransactionTypeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class ExchangeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
