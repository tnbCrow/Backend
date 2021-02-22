def custom_user_authentication_rule(user):
    """
    Override the default user authentication rule for Simple JWT Token to return true if there is a user and let
    serializer check whether user is active or not to return an appropriate error
    :param user: user to be authenticated
    :return: True if user is not None
    """

    return True if user is not None else False
