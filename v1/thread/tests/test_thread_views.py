"""
TODO:
* auth user creates thread
* for the thread creation the two users are required
* done views & serilization task
"""

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
# from django.urls import reverse

from v1.users.tests.test_utils import get_test_user, TEST_PASS


class TestThreadModel(APITestCase):
    def test_auth_user_create_thread_model(self):
        user1, token1 = get_test_user(manual_user="user1")
        user2, token2 = get_test_user(manual_user="user2")

        self.client.login(
            email=user1.email,
            password=TEST_PASS
        )

        print(reverse('thread:thread_list'))
        response = self.client.post(reverse('thread:thread_detail'), data={
            'primary_user': user1.uuid,
            'secondary_user': user2.uuid,
        })

        assert response.status_code == status.HTTP_200_OK
