import json
from django.core import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class AlbumView(GenericAPIView):
    queryset = Album.approved_only.all()
    serializer_class = AlbumSerializer

    def get(self, request):
        ## Preparing Paginator
        paginator = AlbumPagination()

        ## Displaying Paginated Data
        query = paginator.paginate_queryset(queryset=Album.approved_only.all(), request= request)
        data = AlbumSerializer(query, many=True)
        return paginator.get_paginated_response(data.data, status.HTTP_200_OK)



    def post(self, request):

        if request.user.is_authenticated: ## Make sure the user is authenticated

            try: ## Check if the user is an Artist
                artist = request.user.artist_info  ## Get the artist's info
            except Exception as e:
                raise ValidationError("This User is not an Artist.", status.HTTP_403_FORBIDDEN)

            ## Pass the request body to the Album Serializer to validate the Album data
            data = AlbumSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            data.validated_data['artist'] = artist ## Add the Artist
            data.save() ## Save
            return Response(data.data, status=status.HTTP_200_OK)
        else:
            raise ValidationError("Not Authenticated",status.HTTP_403_FORBIDDEN)

