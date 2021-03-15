from rest_framework import serializers

from .models import Country, TransactionType, PaymentMethod, Exchange, Currency


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('__all__')


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = ('uuid', 'name')


class TransactionTypeSerializer(serializers.ModelSerializer):

    payment_method = PaymentMethodSerializer(source='paymentmethod_set', many=True, read_only=True)

    class Meta:
        model = TransactionType
        fields = ('uuid', 'name', 'payment_method')


class ExchangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exchange
        fields = ('__all__')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('__all__')
