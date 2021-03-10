from rest_framework import serializers

from .models import Country, TransactionType, PaymentMethod


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('__all__')


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = ('__all__')


class TransactionTypeSerializer(serializers.ModelSerializer):

    payment_method = PaymentMethodSerializer(source='paymentmethod_set', many=True, read_only=True)

    class Meta:
        model = TransactionType
        fields = ('uuid', 'name', 'payment_method')
