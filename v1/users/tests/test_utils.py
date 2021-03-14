from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken


TEST_PASS = "@Testpass123"

TEST_USER ={
    'email': 'user@example.com',
    'username': 'testuser',
    'password': TEST_PASS,
    're_password': TEST_PASS,
}

@database_sync_to_async
def get_test_user():
    
    #Create user
    user = get_user_model().objects.create_user(
        username=TEST_USER['username'],
        email=TEST_USER['email'],
        password=TEST_USER['password'],
    )

    access = AccessToken.for_user(user)
    return user, access

