from django.urls import path
from .views import ThreadView

app_name = 'thread'
urlpatterns = [
    path('', ThreadView.as_view({'get': 'list'}), name='thread_list'),
    path('<uuid:thread_id>/', ThreadView.as_view({'get': 'retrieve'}), name='thread_detail'),
    path('new/', ThreadView.as_view({'post': 'create'}), name='thread_create')
]
