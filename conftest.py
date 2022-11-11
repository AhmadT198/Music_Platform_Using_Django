import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture(scope="module")
def auth_client():
    '''
    A global fixture "auth_client" that returns a function, if that function is passed a user instance, it'll return an
    instance of DRF's APIClient authenticated by that user instance, otherwise, it'll return an instance of APIClient
    authenticated by an arbitrary user instance.
    '''

    def func(*args, **kwargs):
        client = APIClient()
        if "user" in kwargs:  ## if a user is provided , login and authenticate using this instance
            user = kwargs['user']
            client.force_login(user)
            client.force_authenticate(user)
        else:  ## Else, Create an instance and authenticate using it
            arb_user = User.objects.create_user(username="testuser", password="passwor_d")
            client.force_login(arb_user)
            client.force_authenticate(arb_user)
        return client

    return func
