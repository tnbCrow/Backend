from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.users.models import User
from v1.constants.models import Country


class TierOne(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)

    dob = models.DateField()

    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.is_verified}'
