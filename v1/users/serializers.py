from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('account_number', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at'
