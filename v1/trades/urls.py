from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register('trade-post', views.TradePostViewSet)
router.register('trade-request', views.TradeRequestViewSet, basename='traderequest')
