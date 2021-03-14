from django.db import transaction

from rest_framework import serializers

from .models import TradePost, TradeRequest, ActiveTrade, CompletedTrade

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
        fields = ('uuid', 'post', 'amount', 'message', 'status', 'created_at', 'updated_at')
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
                obj, created = ActiveTrade.objects.get_or_create(post=instance.post, initiator=self.context['request'].user, amount=instance.amount)
        return instance


class ActiveTradeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ActiveTrade
        fields = ('uuid', 'post', 'amount', 'initiator_confirmed', 'owner_confirmed', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'
    
    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super(ActiveTradeSerializer, self).update(instance, validated_data)
        print(instance.post.owner_role)
        if instance.initiator_confirmed and instance.owner_confirmed:
            if instance.post.owner_role == 0:
                buyer = instance.post.owner
                seller = instance.initiator
            else:
                seller = instance.post.owner
                buyer = instance.initiator
            CompletedTrade.objects.create(buyer=buyer, seller=seller, amount=instance.amount)
        return instance
