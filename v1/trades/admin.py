from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Exchange)
admin.site.register(models.PaymentMethod)
admin.site.register(models.TradePost)
admin.site.register(models.TradeRequest)
admin.site.register(models.ActiveTrade)
