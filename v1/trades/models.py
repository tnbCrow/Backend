from uuid import uuid4

from django.utils import timezone
from datetime import timedelta

from django.db import models

from v1.users.models import User
from v1.constants.models import TransactionType, Currency, PaymentMethod, Exchange


# This model is responsible to hold all the tradePost information that the user will create.
class TradePost(models.Model):
    BUYER = 0
    SELLER = 1

    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_role = models.IntegerField(choices=ROLE_CHOICES)

    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    margin = models.IntegerField()
    rate = models.PositiveIntegerField()

    amount = models.PositiveIntegerField()
    payment_windows = models.PositiveIntegerField()

    terms_of_trade = models.TextField()
    min_reputation = models.IntegerField()

    broadcast_trade = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.uuid}: {self.is_active}'


# The initiator will create a tradeRequest if they're interested to make a transaction
# The owner of tradePost will be incharge of accepting or rejecting the trade request.
class TradeRequest(models.Model):
    PENDIGN = 0
    ACCEPTED = 1
    REJECTED = 2
    EXPIRED = 3

    REQUEST_STATUS = [
        (PENDIGN, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (EXPIRED, 'Expired')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    post = models.ForeignKey(TradePost, on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=REQUEST_STATUS, default=0)  # checks if post owner has accepted the trade request

    message = models.CharField(max_length=255)
    amount = models.IntegerField()
    rate = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=timezone.now()+timedelta(days=1))

    def __str__(self):
        return f'{self.post}: {self.status}'


# Once the trade request is accepted, it will be forwarded to this model.
# initiator_confirmed and owner_confirmed flag will be used to confirm both parties have
# sent and recieved the payments
class ActiveTrade(models.Model):
    OPEN = 0
    COMPLETED = 1
    ADMIN_COMPLETED = 2
    OWNER_CANCELLED = 3
    INITIATOR_CANCELLED = 4
    ADMIN_CANCELLED = 5

    STATUS = [
        (OPEN, 'Open'),
        (COMPLETED, 'Completed'),
        (ADMIN_COMPLETED, 'Admin Completed'),
        (OWNER_CANCELLED, 'Owner Cancelled'),
        (INITIATOR_CANCELLED, 'Initiator Cancelled'),
        (ADMIN_CANCELLED, 'Admin Cancelled')
    ]
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    post = models.ForeignKey(TradePost, on_delete=models.CASCADE)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.IntegerField()
    rate = models.PositiveIntegerField()
    status = models.IntegerField(choices=STATUS, default=0)  # status of active trade

    initiator_confirmed = models.BooleanField(default=False)
    owner_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post}'


# once the trade is completed, it will be forwarded to this model.
# Here, the payments will be forwarded to respective personals.
class CompletedTrade(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')

    amount = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.seller} - {self.buyer}: {self.amount}'
