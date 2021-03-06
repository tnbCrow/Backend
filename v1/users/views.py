from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Wallet
from .serializers import WalletCreateSerializer, WalletUpdateSerializer


# Create your views here.
class WalletViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the wallets
        for the currently authenticated user.
        """
        return Wallet.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return WalletCreateSerializer
        else:
            return WalletUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
