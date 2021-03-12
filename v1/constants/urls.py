from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter(trailing_slash=False)
router.register('countries', views.CountryViewSet)
router.register('transaction_type', views.TransactionTypeViewSet)
router.register('exchange', views.ExchangeViewSet)
router.register('currency', views.CurrencyViewSet)
