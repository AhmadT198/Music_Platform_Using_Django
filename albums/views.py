import json
from django.core import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class AlbumView(GenericAPIView):
    queryset = Album.approved_only.all()
    serializer_class = AlbumSerializer
    # pagination_class = AlbumPagination

    def get(self, request):
        ## Preparing Paginator
        paginator = AlbumPagination()

        ## Displaying Paginated Data
        query = paginator.paginate_queryset(queryset=Album.approved_only.all(), request= request)
        data = AlbumSerializer(query, many=True)
        return paginator.get_paginated_response(data.data)



def post(self, request):
   pass
