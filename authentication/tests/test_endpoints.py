import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
def test_register_invalid_data(): ## Testing the Register endpoint for handling invalid data
    client = APIClient()
    User.objects.create_user(username="duplicateTest", password="password")

    invalid_data_list = [
        {   ## Missing Data test
            "username": "testUser"
        },
        {   ##Invalid Email Test
            "username": "testUser",
            "email": "aaaaa",
            "password1": "passwor_d",
            "password2": "passwor_d"
        },
        {   ## Passwords dont match
            "username": "testUser",
            "email": "aaa@aaa.com",
            "password1": "passwor_d2",
            "password2": "passwor_d"
        },
        {   ## Duplicate Username
            "username": "duplicateTest",
            "email": "aaa@aaa.com",
            "password1": "passwor_d",
            "password2": "passwor_d"
        }
    ]

    for invalid_data in invalid_data_list: ## Test each input
        response = client.post("/authentication/register", invalid_data)
        assert response.status_code == 400


@pytest.mark.django_db
def test_register_valid_data(): ## Test the register endpoint for handling valid data
    client = APIClient()
    valid_data = {
        "username": "testregister",
        "email": "aaa@aa.com",
        "password1": "passwor_d",
        "password2": "passwor_d"
    }
    response = client.post("/authentication/register", valid_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_valid_data(auth_client): ## Test the login endpoint for handling valid data
    client = APIClient()
    testuser = User.objects.create_user(username="testuser", password="password")
    valid_data = {
        "username": "testuser",
        "password": "password"
    }
    response = client.post('/authentication/login', valid_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_invalid_data():
    client = APIClient()
    testuser = User.objects.create_user(username="testuser", password="password")
    invalid_data_list = [
        {   ##Blank Username
            "username": "",
            "password": "password"
        },
        {   ##Blank Password
            "username": "testuser",
            "password": ""
        },
        {   ##Non-existing User
            "username": "testuserNotFound",
            "password": "password"
        },
        {   ##Wrong password
            "username": "testuser",
            "password": "passworrd"
        },
    ]
    for invalid_data in invalid_data_list: ## Test each input
        response = client.post('/authentication/login', invalid_data)
        print(response.content)
        assert response.status_code == 400


@pytest.mark.django_db
def test_user_valid(auth_client):  ## Testing the User endpoint


    ## Creating dummy user
    user_data = {
        "username": "ahmadt198",
        "email": "test@email.com",
        "password": "password",
        "bio": "testbio"
    }
    user = User.objects.create_user(**user_data)
    client = auth_client(user=user)

    response = client.get(('/authentication/user/1')) ## Sending POST Request to the endpoint

    ## Extracting data from the response
    actual = {
        "id": response.data['id'],
        "username": response.data['username'],
        "email": response.data['email'],
        "bio": response.data['bio']
    }
    supposed = {
        "id": user.id,
        "username": "ahmadt198",
        "email": "test@email.com",
        "bio": "testbio"
    }

    assert actual == supposed ## Testing the data

@pytest.mark.django_db
def test_user_unauth_access():  ##Testing the User endpoint with Unauthenticated users

    client = APIClient()
    testuser = User.objects.create_user(username="testuser", password="password") ## Creating dummy User
    response = client.get(('/authentication/user/1')) ## Accessing dummy user with no log in

    assert response.status_code == 401


