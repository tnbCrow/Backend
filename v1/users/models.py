from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser

from v1.third_party.tnbCrow.constants import VERIFY_KEY_LENGTH
from v1.third_party.tnbCrow.models import CreatedModified


# Holds the User info.
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)

    first_name = None
    last_name = None

    memo = models.CharField(max_length=44, unique=True, editable=False)

    loaded = models.IntegerField(default=0)  # total coins loaded to the account
    locked = models.IntegerField(default=0)  # coins locked when creating tradePost or tradeRequest

    total_coins_bought = models.IntegerField(default=0)
    total_coins_sold = models.IntegerField(default=0)

    reputation = models.IntegerField(default=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_user_balance(self):
        return self.loaded - self.locked


# Assigns the users with their respective wallets.
# M-T-O with User model
class Wallet(CreatedModified):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username}: {self.account_number}: {self.is_primary}"


# generate a random memo and check if its already taken.
# If taken, generate another memo again until we find a valid memo
def generate_memo(instance):
    memo = f'tnbcrow-{uuid4()}'
    while True:
        if not User.objects.filter(memo=memo).exists():
            return memo


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.memo:
        instance.memo = generate_memo(instance)


# save the memo before the User model is saved with the unique memo
models.signals.pre_save.connect(pre_save_post_receiver, sender=User)
