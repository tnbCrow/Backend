from django.db import transaction

from rest_framework import serializers

from .models import TradePost, TradeRequest, ActiveTrade

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

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super(TradeRequestUpdateSerializer, self).update(instance, validated_data)
        context =self.context['request']
        if 'status' in context.data:
            if context.data['status'] == '1':
                obj, created = ActiveTrade.objects.get_or_create(post=instance.post, initiator=self.context['request'].user)
        return instance
