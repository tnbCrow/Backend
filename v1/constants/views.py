from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
