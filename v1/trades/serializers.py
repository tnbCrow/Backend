from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from v1.constants.models import TransactionFee

from .models import TradePost, TradeRequest, ActiveTrade, CompletedTrade


class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradePost
        fields = ('uuid', 'owner_role', 'currency',
                  'payment_method',
                  'rate', 'amount', 'terms_of_trade', 'min_reputation',
                  'broadcast_trade', 'payment_windows', 'is_active', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at',

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']

        amount = int(validated_data.pop('amount'))  # amount of coins that the user passes in

        # if role's seller, check if they have enough balance. If has enough balance, get the fee percentage,
        # calculate the transaction_fee and determine the post_amount enforcing the fee.
        if context.data['owner_role'] == str(TradePost.SELLER):
            if context.user.get_user_balance() >= amount:
                fee_percentage = TransactionFee.objects.get(id=1).charge / 100
                transaction_fee = int(amount * fee_percentage / 100)
                post_amount = amount - transaction_fee
                validated_data['amount'] = post_amount
                context.user.locked += amount
                context.user.save()
            else:
                error = {'error': 'Please load enough coins into your account'}
                raise serializers.ValidationError(error)
        # If the role is buyer, pass in the amount with no fees.
        else:
            validated_data['amount'] = amount
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
        if post.owner_role == TradePost.BUYER:
            if user.get_user_balance() >= amount:
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
        read_only_fields = 'uuid', 'created_at', 'updated_at', 'post', 'amount', 'message', 'rate', 'expires_at'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        if self.instance.expires_at < timezone.now():
            error = {'error': 'OOps!! Trade request is expired'}
            raise serializers.ValidationError(error)
        elif self.instance.status == TradeRequest.ACCEPTED:
            error = {'error': 'Trade request already accepted'}
            raise serializers.ValidationError(error)
        elif self.instance.status == TradeRequest.REJECTED:
            error = {'error': 'You cannot undo a rejected trade request'}
            raise serializers.ValidationError(error)
        elif self.instance.status == TradeRequest.CANCELLED:
            error = {'error': 'You cannot undo a cancelled trade request'}
            raise serializers.ValidationError(error)
        elif self.instance.status == TradeRequest.EXPIRED:
            error = {'error': 'You cannot undo a expired trade request'}
            raise serializers.ValidationError(error)

        instance = super(TradeRequestUpdateSerializer, self).update(instance, validated_data)
        if 'status' in context.data:
            if context.data['status'] == str(TradeRequest.ACCEPTED):
                instance.post.amount -= int(context.data['amount'])
                instance.post.save()
                obj, created = ActiveTrade.objects.get_or_create(post=instance.post,
                                                                 initiator=instance.initiator,
                                                                 amount=instance.amount,
                                                                 rate=instance.rate,
                                                                 payment_windows=instance.payment_windows,
                                                                 terms_of_trade=instance.terms_of_trade,
                                                                 payment_method=instance.payment_method)
            elif context.data['status'] == str(TradeRequest.REJECTED) or context.data['status'] == str(TradeRequest.CANCELLED):
                if self.instance.post.owner_role == TradePost.BUYER:
                    user = context.user
                    user.locked -= self.instance.amount
                    user.save()
        return instance


class ActiveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveTrade
        fields = ('uuid', 'post', 'amount', 'initiator_confirmed', 'owner_confirmed', 'created_at', 'updated_at', 'status')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        payment_windows_expires_at = instance.created_at + timedelta(minutes=instance.payment_windows)

        if self.instance.status == ActiveTrade.COMPLETED or self.instance.status == ActiveTrade.ADMIN_COMPLETED or self.instance.status == ActiveTrade.OWNER_CANCELLED or self.instance.status == ActiveTrade.INITIATOR_CANCELLED or self.instance.status == ActiveTrade.ADMIN_CANCELLED:
            error = {'error': 'You cannot undo the action'}
            raise serializers.ValidationError(error)

        if 'status' in context.data:
            if context.data['status'] == str(ActiveTrade.COMPLETED) or context.data['status'] == str(ActiveTrade.ADMIN_COMPLETED) or context.data['status'] == str(ActiveTrade.ADMIN_CANCELLED):
                error = {'error': 'You cannot set this status'}
                raise serializers.ValidationError(error)
            elif payment_windows_expires_at > timezone.now():
                if (instance.post.owner_role == TradePost.BUYER and context.data['status'] == str(ActiveTrade.INITIATOR_CANCELLED)) or (instance.post.owner_role == TradePost.SELLER and context.data['status'] == str(ActiveTrade.OWNER_CANCELLED)):
                    error = {'error': 'Payment window must expire before cancelling the ActiveTrade'}
                    raise serializers.ValidationError(error)

        instance = super(ActiveTradeSerializer, self).update(instance, validated_data)
        if instance.initiator_confirmed and instance.owner_confirmed:
            if instance.post.owner_role == TradePost.BUYER:
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


class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradePost
        fields = ('amount', )
