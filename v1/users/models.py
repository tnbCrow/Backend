from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from v1.third_party.tnbCrow.constants import VERIFY_KEY_LENGTH
from v1.third_party.tnbCrow.models import CreatedModified

# Create your models here.
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)

    first_name = None
    last_name = None

    memo = models.CharField(max_length=44, default="tnbcrow-"+ str(uuid4), unique=True,  editable=False)
    balance = models.PositiveBigIntegerField(default=0)
    reputation = models.IntegerField(default=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Wallet(CreatedModified):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username}: {self.account_number}: {self.is_primary}"
