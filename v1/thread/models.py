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

    def is_user_allowed(self, user):
        if user == self.primary_user:
            return True
        if user == self.secondary_user:
            return True
        if user == self.admin_user:
            return True
        return False

    def validate_thread(thread_ud):
        thread = ChatThread.objects.filter(uuid=thread_ud).first()
        if thread is not None:
            return True
        return False
