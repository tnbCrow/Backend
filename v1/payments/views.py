import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

PV_IP = "54.219.183.128"
BANK_IP = "54.177.121.3"
ESCROW_WALLET = "5ad13fd8cc674da7a3ad35426e0fcfe3a3157a044ebda0f54b9b32ee873ea921"
TRANSACTION_URL = f"http://{BANK_IP}/bank_transactions?account_number=&block__sender={ESCROW_WALLET}&fee=&recipient="


class ChainScan(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        r = requests.get(TRANSACTION_URL).json()
        print(request.user.memo)
        return Response(status=status.HTTP_201_CREATED)
