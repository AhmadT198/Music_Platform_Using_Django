from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class Login(View):

    def post(self, request):

        try:
            ## Get data from the request body and Extract the username and password.
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            ## Verify the user's Credentials
            user = authenticate(request, username=username, password=password)

            ## if the user exists:
            if user is not None:
                print("logged in as ", user)
                login(request, user) ## Login
                return JsonResponse({"message": "Log In Successful."}, status=200) ## Return a Success Message
            else:
                return JsonResponse({"message": "Invalid Username and/or Password"}, status=403)


        except Exception as e: ## Return Error if it occurs
            return JsonResponse({"type": str(e.__class__.__name__), "message" : str(e)}, status=500)
