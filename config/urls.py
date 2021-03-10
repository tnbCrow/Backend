from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from v1.constants.urls import router as constants_router

admin.site.index_title = 'Admin'
admin.site.site_header = 'tnbCrow'
admin.site.site_title = 'tnbCrow'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('v1.third_party.rest_framework_simplejwt.urls')),
]

router = DefaultRouter(trailing_slash=False)
router.registry.extend(constants_router.registry)
urlpatterns += router.urls
