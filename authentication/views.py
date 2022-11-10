from django.utils import timezone
from hashlib import sha512
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, permissions, status
from rest_framework import generics
from knox.views import LoginView as KnoxLoginView,LogoutView as KnoxLogoutView,LogoutAllView as KnoxLogoutAllView
from django.contrib.auth.signals import user_logged_in, user_logged_out

from users.models import User

from .serializers import *


# Create your views here.


class Register(APIView):
    '''Class based View to handle registeration through the endpoint /authentication/register '''

    def post(self, request, *args, **kwargs):
        data = RegisterSerializer(data=request.data)  ## Pass the request body to the UserSerializer
        data.is_valid(raise_exception=True)  ##if the data is valid.
        user = data.save()  # Create the User
        return Response({
            "message": f"{user} Registered Successfully !"
        }, status=200)  ## Return Success Message


####### Example Input
# {
#     "email": "asas@aaa.com",
#     "username": "asasas",
#     "password1": "aaaaaaa_a",
#     "password2": "aaaaaaa_a"
# }