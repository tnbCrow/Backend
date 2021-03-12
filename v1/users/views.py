from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Wallet
from .serializers import WalletSerializer

# Create your views here.
class WalletViewSet(viewsets.ModelViewSet):

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the wallets
        for the currently authenticated user.
        """
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user)
        return query_set

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
