from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Exchange)
admin.site.register(models.TransactionType)
admin.site.register(models.Currency)
