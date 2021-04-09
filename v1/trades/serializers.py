from django.db import transaction

from rest_framework import serializers

from .models import TradePost, TradeRequest, ActiveTrade, CompletedTrade


class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePost
        fields = ('uuid', 'owner_role', 'transaction_type', 'currency',
                  'payment_method', 'exchange', 'margin',
                  'rate', 'amount', 'terms_of_trade', 'min_reputation',
                  'broadcast_trade', 'is_active', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'rate',

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']
        user = context.user
        amount = int(context.data['amount'])
        if context.data['owner_role'] == '1':
            if int(user.loaded) - int(user.locked) >= amount:
                user.locked += amount
                user.save()
            else:
                error = {'error': 'Please load enough coins into your account'}
                raise serializers.ValidationError(error)
        instance = super(TradePostSerializer, self).create(validated_data)
        return instance


class TradeRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'amount', 'rate', 'message', 'status', 'created_at', 'updated_at', 'expires_at')
        read_only_fields = 'created_at', 'updated_at', 'status', 'rate', 'expires_at'

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']
        amount = int(context.data['amount'])

        if self.validated_data['post'].amount <= amount:
            error = {'error': 'Amount has exceeded the trade amount'}
            raise serializers.ValidationError(error)

        user = context.user
        post = self.validated_data['post']
        if post.owner_role == 0:
            if int(user.loaded) - int(user.locked) >= amount:
                user.locked += amount
                user.save()
            else:
                error = {'error': 'Please load enough coins into your account'}
                raise serializers.ValidationError(error)
            post.amount -= amount
            post.save()

        instance = super(TradeRequestCreateSerializer, self).create(validated_data)

        return instance


class TradeRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeRequest
        fields = ('uuid', 'post', 'status', 'rate', 'amount', 'message', 'created_at', 'updated_at', 'expires_at')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount', 'message', 'rate', 'expires_at'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        if self.instance.status == 1:
            error = {'error': 'Trade request already accepted'}
            raise serializers.ValidationError(error)

        elif self.instance.status == 2:
            error = {'error': 'You cannot undo a rejected trade request'}
            raise serializers.ValidationError(error)

        instance = super(TradeRequestUpdateSerializer, self).update(instance, validated_data)
        if 'status' in context.data:
            if context.data['status'] == '1':
                instance.post.amount -= int(context.data['amount'])
                instance.post.save()
                obj, created = ActiveTrade.objects.get_or_create(post=instance.post, initiator=instance.initiator, amount=instance.amount, rate=instance.rate)
            elif context.data['status'] == '2':
                if self.instance.post.owner_role == 0:
                    user = context.user
                    user.locked -= self.instance.amount
                    user.save()
            return instance


class ActiveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveTrade
        fields = ('uuid', 'post', 'amount', 'initiator_confirmed', 'owner_confirmed', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super(ActiveTradeSerializer, self).update(instance, validated_data)
        if instance.initiator_confirmed and instance.owner_confirmed:
            if instance.post.owner_role == 0:
                buyer = instance.post.owner
                seller = instance.initiator
            else:
                seller = instance.post.owner
                buyer = instance.initiator
            user = self.context['request'].user
            user.loaded += instance.amount
            user.locked -= instance.amount
            user.save()
            CompletedTrade.objects.create(buyer=buyer, seller=seller, amount=instance.amount)
        return instance
