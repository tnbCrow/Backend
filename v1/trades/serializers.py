from rest_framework import serializers

from .models import TradePost

class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePost
        fields = ('owner_role', 'transaction_type', 'currency', 'payment_method', 'exchange', 'margin',\
             'amount', 'terms_of_trade', 'min_reputation', 'broadcast_trade', 'is_active',)
