from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatThread(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    primary_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='primary_threads')
    secondary_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scondary_threads')
    admin_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='dispute_threads', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
