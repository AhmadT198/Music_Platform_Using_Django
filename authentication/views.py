from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

from users.models import User

from .serializers import UserSerializer


# Create your views here.


class Register(APIView):
    '''Class based View to handle registeration through the endpoint /authentication/register '''


    def post(self, request, *args, **kwargs):
        data = UserSerializer(data=request.data) ## Pass the request body to the UserSerializer
        if data.is_valid(): ##if the data is valid.
            user = User.objects.create_user(data.data['username'], data.data['email'].lower(), data.data['password1']) #Create the User
            return Response({"message" : f"{user} Registered Successfully !"},status=200) ## Return Success Message
        return Response(data.errors, status=500) ##Else Return the occuring error



####### Example Input
# {
#     "email": "asas@aaa.com",
#     "username": "asasas",
#     "password1": "aaaaaaa_a",
#     "password2": "aaaaaaa_a"
# }