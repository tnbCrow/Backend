from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from django.db.models import Q

from v1.third_party.tnbCrow.permissions import IsOwner, ReadOnly
from v1.constants.models import TransactionFee

from .models import TradePost, TradeRequest, ActiveTrade
from .serializers import TradePostSerializer, TradeRequestCreateSerializer,\
    TradeRequestUpdateSerializer, ActiveTradeSerializer, AmountSerializer
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
        serializer.save(owner=self.request.user)

    @action(methods=['post'], detail=True)
    def load(self, request, **kwargs):

        obj = self.get_object()

        # self.serializer_class = AmountSerializer
        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():
            amount = int(request.data['amount'])
            if obj.owner_role == TradePost.SELLER:
                if request.user.get_user_balance() > amount:
                    request.user.locked += amount
                    fee_percentage = TransactionFee.objects.get(id=1).charge / 100
                    transaction_fee = int(amount * fee_percentage / 100)
                    final_amount = amount - transaction_fee
                    obj.amount += final_amount
                    obj.save()
                    request.user.save()
                else:
                    error = {'error': 'You donot have enough balance to load!!'}
                    raise serializers.ValidationError(error)
            else:
                obj.amount += amount
                obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def withdraw(self, request, **kwargs):

        obj = self.get_object()

        # self.serializer_class = AmountSerializer
        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():
            amount = int(request.data['amount'])
            if obj.amount >= amount:
                if obj.owner_role == TradePost.SELLER:
                    fee_percentage = TransactionFee.objects.get(id=1).charge / 100
                    final_amount = (amount * 100) / (100 - fee_percentage)
                    request.user.locked -= final_amount
                    obj.amount -= amount
                    obj.save()
                    request.user.save()
                else:
                    obj.amount -= amount
                    obj.save()
            else:
                error = {'error': 'Trade Post donot have enough coins to withdraw!!'}
                raise serializers.ValidationError(error)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            trade_requests = TradeRequest.objects.filter(Q(initiator=self.request.user) | Q(post__owner=self.request.user))
            expired_requests = trade_requests.filter(expires_at__lte=timezone.now())
            expired_requests.update(status=TradeRequest.EXPIRED)
            for request in expired_requests:
                if request.post.owner_role == TradePost.BUYER:
                    request.initiator.locked -= request.amount
                    request.initiator.save()
            return trade_requests
        else:
            return TradeRequest.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TradeRequestCreateSerializer
        else:
            return TradeRequestUpdateSerializer

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update':
            if self.request.data['status'] == str(TradeRequest.ACCEPTED) or self.request.data['status'] == str(TradeRequest.REJECTED):
                return [TradeRequestPostOwner(), ]
            elif self.request.data['status'] == str(TradeRequest.CANCELLED):
                return [TradeRequestInitiator(), ]
            elif self.request.data['status'] == str(TradeRequest.EXPIRED):
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
            if data['status'] == str(ActiveTrade.OWNER_CANCELLED):
                return [TradeRequestPostOwner(), ]
            elif data['status'] == str(ActiveTrade.INITIATOR_CANCELLED):
                return [TradeRequestInitiator(), ]
        if 'initiator_confirmed' in data and 'owner_confirmed' not in data:
            return [TradeRequestInitiator(), ]
        elif 'owner_confirmed' in data and 'initiator_confirmed' not in data:
            return [TradeRequestPostOwner(), ]
        else:
            return [IsAuthenticated(), ]
