from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework import status


TEST_PASS = "@Testpass123"
TEST_USER ={
    'email': 'user@example.com',
    'username': 'testuser',
    'password': TEST_PASS,
    're_password': TEST_PASS,
}

class AuthneticationTest(APITestCase):
    def create_test_user(self):
        user_model = get_user_model()
        user = user_model.objects.create(
            username=TEST_USER.get('username'),
            email=TEST_USER.get('email'),
            password=TEST_USER.get('password'),
        )
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
        print(user.email)
        response = self.client.post(reverse('jwt-create'), data={
            'email': user.email,
            'password': TEST_PASS,
        })

        assert status.HTTP_200_OK == response.status_code
        assert response.data.get("acess") is not None