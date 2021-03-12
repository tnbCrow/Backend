from rest_framework import serializers

from .models import Wallet


class WalletCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'account_number', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'is_primary',


class WalletUpdateSerializer(WalletCreateSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'account_number', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at'
