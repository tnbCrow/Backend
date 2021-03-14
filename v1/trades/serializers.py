from rest_framework import serializers

from .models import TradePost, TradeRequest

class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePost
        fields = ('uuid', 'owner_role', 'transaction_type', 'currency',\
                'payment_method', 'exchange', 'margin',\
                'rate', 'amount', 'terms_of_trade', 'min_reputation',\
                'broadcast_trade', 'is_active', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'rate',


class TradeRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'status', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'status',


class TradeRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'status', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'post'
