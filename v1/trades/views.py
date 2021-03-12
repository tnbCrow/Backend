from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from v1.constants.models import Exchange

from .models import TradePost
from .serializers import TradePostSerializer

# Create your views here.
class TradePostViewSet(viewsets.ModelViewSet):

    queryset = TradePost.objects.all()
    serializer_class = TradePostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        exchange_price = Exchange.objects.get(uuid=self.request.data['exchange']).price
        rate = exchange_price * (100+int(self.request.data['margin']))/100
        serializer.save(owner=self.request.user, rate=rate)
