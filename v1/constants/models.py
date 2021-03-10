from uuid import uuid4

from django.db import models


class Exchange(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.price}'


class TransactionType(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ['type', 'name']

    def __str__(self):
        return f'{self.type.name}: {self.name}'


class Currency(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f'{self.name}'


class TransactionFee(models.Model):
    name = models.CharField(max_length=255, unique=True)
    charge = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.charge}'


class Country(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    alpha_two_code = models.CharField(max_length=2)
    alpha_three_code = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.alpha_two_code}: {self.name}'
        