from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Exchange)
admin.site.register(models.TransactionType)
admin.site.register(models.Currency)
admin.site.register(models.TransactionFee)
admin.site.register(models.PaymentMethod)
