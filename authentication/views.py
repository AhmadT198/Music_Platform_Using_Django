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
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView
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

class Login(KnoxLoginView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):

        ## Check User Credentials
        data = loginSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        user = authenticate(**data.data)
        if user is None:
            raise ValidationError("Invalid Username and/or Password.")

        ## If True, Check the number of tokens he has
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )

        ## If number of tokens did not exceed the maximum, Log the user in
        login(request, user)

        token_ttl = self.get_token_ttl()
        token = AuthToken.objects.create(user, token_ttl)[1]  ## Create Token for User
        user_logged_in.send(sender=user.__class__,
                            request=request, user=user)


        ## Return the user data
        data = {
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": user.bio
            }
        }

        return Response(data, status=status.HTTP_200_OK)


class Logout(KnoxLogoutView):
    def post(self, request, format=None):
        request._auth.delete() ## Delete the Current User's token
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response("Logged Out Successfully!", status=status.HTTP_204_NO_CONTENT)


class LogoutAll(KnoxLogoutAllView):
    def post(self, request, format=None):
        request.user.auth_token_set.all().delete() ## Delete all current User's tokens, to close all sessions
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response("All Current Sessions have been Logged Out successfully !", status=status.HTTP_204_NO_CONTENT)


class UserAPI(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            user = User.objects.get(id=pk) ## Get the user

            ## Extract the data
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": user.bio
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e: ## Return Error
            return Response({"message": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']

        ## Check if the current user has permission
        if request.user.id != pk:
            return Response("Permission Denied", status=status.HTTP_403_FORBIDDEN)

        try:
            data = UpdateSerializer(data=request.data) ## Pass the data to the UpdateSerializer

            if data.is_valid(): ## if the Request Data is valid
                user = User.objects.get(id=pk)

                ## Update and save
                user.username = data.data['username']
                user.email = data.data['email']
                user.bio = data.data['bio']
                user.save()

                return Response(data.data, status=status.HTTP_200_OK) ## Return the Updated Data
            return Response(data.errors) ## Return Form Errors

        except Exception as e:
            return Response({"message": "User Not Found !"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):

        pk = kwargs['pk']
        ## Check if the current user has permission
        if request.user.id != pk:
            return Response("Permission Denied", status=status.HTTP_403_FORBIDDEN)

        try:
            data = PatchSerializer(data=request.data) ## Pass the data to the PatchSerializer
            if data.is_valid():
                user = User.objects.get(id=pk)

                ## Update the provided data only
                if 'username' in data.data.keys():
                    user.username = data.data['username']
                if 'email' in data.data.keys():
                    user.email = data.data['email']
                if 'bio' in data.data.keys():
                    user.bio = data.data['bio']
                user.save()

                return Response(data.data, status=status.HTTP_200_OK)## Return the Updated Data
            return Response(data.errors) ## Return Form Errors
        except Exception as e:
            return Response({"message": "User Not Found !"}, status=status.HTTP_404_NOT_FOUND)
