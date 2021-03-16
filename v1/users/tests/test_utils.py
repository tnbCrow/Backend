from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken


TEST_PASS = "@Testpass123"

TEST_USER = {
    'email': 'user@example.com',
    'username': 'testuser',
    'password': TEST_PASS,
    're_password': TEST_PASS,
}


def get_test_user(user_info=TEST_USER, manual_user=None):
    # user credentilas
    username = user_info['username']
    email = user_info['email']

    # use custom credentilas
    if manual_user:
        username = manual_user
        email = f"{username}@gmail.com"

    # Create user
    user = get_user_model().objects.create_user(
        username,
        email,
        password=user_info['password'],
    )

    access = AccessToken.for_user(user)
    return user, access


@database_sync_to_async
def get_test_user_async(user_info=TEST_USER, manual_user=None):
    return get_test_user(user_info=TEST_USER, manual_user=None)
