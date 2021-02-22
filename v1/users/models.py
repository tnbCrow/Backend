import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']