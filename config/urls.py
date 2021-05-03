from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from v1.constants.urls import router as constants_router
from v1.trades.urls import router as trades_router
from v1.users.urls import router as users_router

# Swagger Thing
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.index_title = 'Admin'
admin.site.site_header = 'tnbCrow'
admin.site.site_title = 'tnbCrow'

schema_view = get_schema_view(
    openapi.Info(
        title="tnbCrow API",
        default_version='v1',
        description="Open API Docs for tnbCrow",
        terms_of_service="https://github.com/tnbCrow",
        contact=openapi.Contact(email="tnbcrow@gmail.com"),
        license=openapi.License(name="GNU GENERAL PUBLIC LICENSE"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('v1.third_party.rest_framework_simplejwt.urls')),
    path('api/chat/', include('v1.thread.urls', 'thread')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

router = DefaultRouter(trailing_slash=False)
router.registry.extend(constants_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(trades_router.registry)
urlpatterns += router.urls


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
