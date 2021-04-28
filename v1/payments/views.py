import requests
from django.utils import timezone
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

PV_IP = "54.219.183.128"
BANK_IP = "54.177.121.3"
ESCROW_WALLET = "22d0f0047b572a6acb6615f7aae646b0b96ddc58bfd54ed2775f885baeba3d6a"
TRANSACTION_URL = f"http://{BANK_IP}/bank_transactions?account_number=&block__sender=&fee=&recipient={ESCROW_WALLET}"


class ChainScan(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        r = requests.get(TRANSACTION_URL).json()
        for transaction in r['results']:
            transaction_time = timezone.make_aware(datetime.strptime(transaction['block']['modified_date'], '%Y-%m-%dT%H:%M:%S.%fZ'))
            if timezone.now() > transaction_time:
                print("Yeah")
                break
        return Response(status=status.HTTP_201_CREATED)
