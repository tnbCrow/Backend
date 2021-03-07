from uuid import uuid4

from django.db import models

from v1.users.models import User


class Exchange(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.price}'


class PaymentMethod(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
class TradePost(models.Model):
    BUY = 0
    SELL = 1

    TRADE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    trade_type = models.IntegerField(choices=TRADE_CHOICES)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    margin = models.IntegerField(default=100)
    price = models.IntegerField()

    min_transaction = models.IntegerField()
    max_transaction = models.IntegerField()

    is_active = models.BooleanField(default=False)
    terms_of_trade = models.TextField()
    broadcast_trade = models.BooleanField(default=False)
    min_reputation = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.uuid}: {self.is_active}'


class TradeRequest(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    post = models.ForeignKey(TradePost, on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)             # checks if post owner has accepted the trade request

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post}: {self.is_accepted}'


class ActiveTrade(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    post = models.ForeignKey(TradePost, on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    initiator_confirmed = models.BooleanField(default=False)
    owner_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post


class CompletedTrade(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.seller} - {self.buyer}: {self.amount}'
