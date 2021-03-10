from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

from .models import Country, TransactionType
from .serializers import CountrySerializer, TransactionTypeSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TransactionTypeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
