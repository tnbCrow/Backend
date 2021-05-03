from django.db.models import Q
from rest_framework import permissions, viewsets
from .models import ChatThread
from .serializers import ThreadSerializer


class ThreadView(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'thread_id'

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ThreadSerializer

    def get_queryset(self):
        user = self.request.user
        return ChatThread.objects.filter(
            Q(primary_user=user) | Q(secondary_user=user)
        )
