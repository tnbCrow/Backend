import base64
import json

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from .test_utils import TEST_USER, TEST_PASS


class AuthneticationTest(APITestCase):
    def create_test_user(self):
        _ = self.client.post(reverse('user-list'), data=TEST_USER)
        user = get_user_model().objects.last()
        return user

    def test_user_register(self):
        response = self.client.post(reverse('user-list'), data=TEST_USER)
        user = get_user_model().objects.last()

        assert status.HTTP_201_CREATED == response.status_code
        assert response.data['uuid'] == str(user.uuid)
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email

    def test_user_sigin_in(self):
        user = self.create_test_user()
        response = self.client.post(reverse('jwt-create'), data={
            'email': user.email,
            'password': TEST_PASS,
        })

        # Login success
        assert status.HTTP_200_OK == response.status_code

        # Parsing payload data from access token.
        assert response.data.get("access") is not None
        access = response.data['access']
        _, payload, _ = access.split('.')
        decoded_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decoded_payload)

        # Get uiid of same user
        assert payload_data.get('user_id') == str(user.uuid)
