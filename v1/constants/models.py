from uuid import uuid4

from django.db import models


class Exchange(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.price}'


class TransactionType(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Currency(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class TransactionFee(models.Model):
    name = models.CharField(max_length=255)
    charge = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.charge}'
