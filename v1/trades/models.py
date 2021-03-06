from uuid import uuid4

from django.db import models

from v1.users.models import User

from thenewboston.constants.network import VERIFY_KEY_LENGTH

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
    final_price = models.IntegerField()

    min_transaction = models.IntegerField()
    max_transaction = models.IntegerField()

    is_active = models.BooleanField(default=False)
    terms_of_trade = models.TextField()

    min_reputation = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.uuid}: {self.is_active}'
