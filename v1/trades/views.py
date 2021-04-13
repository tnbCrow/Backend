from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS

from django.db.models import Q

from v1.constants.models import Exchange
from v1.third_party.tnbCrow.permissions import IsOwner, ReadOnly

from .models import TradePost, TradeRequest, ActiveTrade
from .serializers import TradePostSerializer, TradeRequestCreateSerializer, TradeRequestUpdateSerializer, ActiveTradeSerializer
from .permissions import TradeRequestInitiator, TradeRequestPostOwner


class TradePostViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):

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
        rate = exchange_price * (100 + int(self.request.data['margin'])) / 100
        serializer.save(owner=self.request.user, rate=rate)


class TradeRequestViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        """
        This view should return a list of all the wallets
        for the currently authenticated user.
        """
        if self.request.method in SAFE_METHODS:
            return TradeRequest.objects.filter(Q(initiator=self.request.user) | Q(post__owner=self.request.user))
        else:
            return TradeRequest.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TradeRequestCreateSerializer
        else:
            return TradeRequestUpdateSerializer

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update':
            if self.request.data['status'] == '1' or self.request.data['status'] == '2':
                return [TradeRequestPostOwner(), ]
            elif self.request.data['status'] == '3':
                return [TradeRequestInitiator(), ]
            elif self.request.data['status'] == '4':
                return [ReadOnly(), ]
            else:
                return [IsAuthenticated(), ]
        else:
            return [IsAuthenticated(), ]

    def perform_create(self, serializer):
        post = TradePost.objects.get(uuid=self.request.data['post'])
        serializer.save(initiator=self.request.user, rate=post.rate, payment_windows=post.payment_windows, payment_method=post.payment_method, terms_of_trade=post.terms_of_trade)


class ActiveTradeViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        """
        This view should return a list of all the wallets
        for the currently authenticated user.
        """
        return ActiveTrade.objects.filter(Q(initiator=self.request.user) | Q(post__owner=self.request.user))

    serializer_class = ActiveTradeSerializer

    def get_permissions(self):
        data = self.request.data
        if 'status' in data:
            if data['status'] == '3':
                return [TradeRequestPostOwner(), ]
            elif data['status'] == '4':
                return [TradeRequestInitiator(), ]
        if 'initiator_confirmed' in data and 'owner_confirmed' not in data:
            return [TradeRequestInitiator(), ]
        elif 'owner_confirmed' in data and 'initiator_confirmed' not in data:
            return [TradeRequestPostOwner(), ]
        else:
            return [IsAuthenticated(), ]
