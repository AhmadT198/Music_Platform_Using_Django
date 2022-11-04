from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from artists.forms import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class artist(View):
    def get(self, request): ## Unauthenticated Users can view the artists freely
        print(request.user)
        data = serializers.serialize('json',Artist.objects.all())
        return JsonResponse(json.loads(data), safe=False, status=200)

    def post(self, request):
        if (request.user.is_authenticated): ## Only Authenticated Users can Add Artists
            try:

                ## Pass the data to the ArtistForm
                data = ArtistForm(data=json.loads(request.body))
                if data.is_valid(): ## if it is Valid
                    data.save() ## Save and return the new data
                    return JsonResponse(data.data)
                return JsonResponse(data.errors, status=422) ## if not valid, return the errors
            except:
                return JsonResponse({"message" : "Unknown Format."}, status=500)

        else: ## ELse, if not authenticated
            return JsonResponse({"message": "Please log in"}, status=500)


