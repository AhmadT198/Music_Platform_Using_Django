import json
from django.core import serializers
from django.http import JsonResponse
from django.views import View
from .forms import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from .models import *

class album(View):

    def get(self, request):
        print(request.user)
        # print(request.user.get_all_permissions())
        # print(Permission.objects.all())
        if (request.user.is_authenticated and request.user.has_perm('albums.view_album')): ## If the current User has permission to view the Album Data

            ## Get Queryset and prepare its format then return it in JSON format
            data = Album.objects.all()
            data = serializers.serialize('json', data)
            data = json.loads(data)
            return JsonResponse(data, safe=False)

        else: ## Else Raise an exception if the user is unauthorized
            raise PermissionDenied

    def post(self, request):
        print(request.user)
        if request.user.is_authenticated and request.user.has_perm('albums.add_album'): ### If the current User the permission to ADD data to the Album Model
            try:
                ## Pass the data to the AlbumForm
                data = AlbumForm(json.loads(request.body))
                if data.is_valid(): ## If the data is Valid, Save it and return the added data
                    data.save()
                    return JsonResponse(data.data, status=200)
                return JsonResponse(data.errors, status=422) ## Else return any existing Errors

            except Exception as e:
                return JsonResponse({"message" : str(e)}, status=500)

        else: ### Else, raise an exception if the user is unauthorized
            raise PermissionDenied

