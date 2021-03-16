from django.test import TestCase
from v1.users.tests.test_utils import get_test_user
from v1.thread.models import ChatThread


class TestThreadModel(TestCase):
    def test_can_create_thread_model(self):
        user1, _ = get_test_user(manual_user="test1")
        user2, _ = get_test_user(manual_user="test2")
        chat_thread = ChatThread(primary_user=user1, secondary_user=user2)
        assert chat_thread.primary_user == user1

