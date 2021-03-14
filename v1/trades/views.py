from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS

from django.db.models import Q

from v1.constants.models import Exchange
from v1.third_party.tnbCrow.permissions import IsOwner

from .models import TradePost, TradeRequest, ActiveTrade
from .serializers import TradePostSerializer, TradeRequestCreateSerializer, TradeRequestUpdateSerializer, ActiveTradeSerializer
from .permissions import TradeRequestInitiator, TradeRequestPostOwner

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

    def get_queryset(self):
        """
        This view should return a list of all the wallets
        for the currently authenticated user.
        """
        if self.request.method in SAFE_METHODS:
            return TradeRequest.objects.filter(Q(initiator=self.request.user, status=0)|Q(post__owner=self.request.user, status=0))
        else:
            return TradeRequest.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TradeRequestCreateSerializer
        else:
            return TradeRequestUpdateSerializer
    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return [TradeRequestInitiator(), ]
        elif self.action == 'partial_update' or self.action =='update':
            return [TradeRequestPostOwner(), ]
        else:
            return [IsAuthenticated(), ]

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)

class ActiveTradeViewSet(viewsets.ModelViewSet):

    queryset = ActiveTrade.objects.all()
    serializer_class = ActiveTradeSerializer

    def get_permissions(self):
        data = self.request.data
        if 'initiator_confirmed' in data and not 'owner_confirmed' in data:
            return [TradeRequestInitiator(), ]
        elif 'owner_confirmed' in data and not 'initiator_confirmed' in data:
            return [TradeRequestPostOwner(), ]
        else:
            return [IsAuthenticated(), ]
