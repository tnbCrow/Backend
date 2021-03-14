from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

#TODO: Add the tests for the authnetication
TEST_PASS = "@Testpass123"



class AuthneticationTest(APITestCase):
    def test_user_register(self):
        response = self.client.post(reverse('sign_up'), data={
            'email': 'user@example.com',
            'username': 'testuser',
            'password': TEST_PASS,
        })        


    def test_user_sigin_in(self):
        assert 1 == 1 