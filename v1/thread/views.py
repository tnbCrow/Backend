from rest_framework import permissions, viewsets


class ThreadView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'thread_id'

    permission_classes = (permissions.IsAuthenticated,)
