"""
TODO:
* auth user creates thread
* for the thread creation the two users are required
* done views & serilization task
"""

# from v1.thread.models import ChatThread
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

# from django.urls import reverse
from v1.users.tests.test_utils import get_test_user


class TestThreadModel(APITestCase):
    def test_auth_user_create_thread_model(self):
        user1, token1 = get_test_user(manual_user="user1")
        user2, _ = get_test_user(manual_user="user2")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token1))
        response = self.client.post(reverse('thread:thread_create'), data={
            'primary_user': user1.uuid,
            'secondary_user': user2.uuid,
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('primary_user') == user1.uuid
        assert response.data.get('secondary_user') == user2.uuid

    def test_user_can_only_view_their_threads(self):
        user1, token1 = get_test_user(manual_user="user1")
        user2, _ = get_test_user(manual_user="user2")
        user3, token3 = get_test_user(manual_user="user3")

        # create thread 1 (user1 & user2)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token1))
        self.client.post(reverse('thread:thread_create'), data={
            'primary_user': user1.uuid,
            'secondary_user': user2.uuid,
        })

        # create thread 2 (user1 & user3)
        self.client.post(reverse('thread:thread_create'), data={
            'primary_user': user1.uuid,
            'secondary_user': user3.uuid,
        })

        # login as user 3
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token3))
        response = self.client.get(reverse('thread:thread_list'))
        assert response.status_code == status.HTTP_200_OK
        threads = response.data

        # assert user2 info is not shown
        for thread in threads:
            print(thread.get("primary_user"))
            assert thread.get("secondary_user") != user2.uuid

    def test_unauth_user_cant_create_thread(self):
        user1, _ = get_test_user(manual_user="user1")
        user2, _ = get_test_user(manual_user="user2")

        response = self.client.post(reverse('thread:thread_create'), data={
            'primary_user': user1.uuid,
            'secondary_user': user2.uuid,
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
