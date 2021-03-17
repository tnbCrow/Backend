from rest_framework.reverse import reverse
from rest_framework import serializers, status

from ..factories.user import WalletFactory

def test_wallet_list(api_client, django_assert_max_num_queries):
    pass
