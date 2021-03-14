from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS

from v1.constants.models import Exchange
from v1.third_party.tnbCrow.permissions import IsOwner

from .models import TradePost, TradeRequest
from .serializers import TradePostSerializer, TradeRequestCreateSerializer, TradeRequestUpdateSerializer

# Create your views here.
class TradePostViewSet(viewsets.ModelViewSet):

    queryset = TradePost.objects.all()
    serializer_class = TradePostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny(), ]
        elif self.action == 'create':
            return [IsAuthenticated(), ]
        else:
            return [IsOwner(), ]

    def perform_create(self, serializer):
        exchange_price = Exchange.objects.get(uuid=self.request.data['exchange']).price
        rate = exchange_price * (100+int(self.request.data['margin']))/100
        serializer.save(owner=self.request.user, rate=rate)


class TradeRequestViewSet(viewsets.ModelViewSet):

    queryset = TradeRequest.objects.all()
    serializer_class = TradeRequestCreateSerializer
