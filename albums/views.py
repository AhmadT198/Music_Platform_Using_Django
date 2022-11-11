import json
from django.core import serializers
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class AlbumFilter(django_filters.FilterSet):  ## Album Filtering Class
    cost = django_filters.NumberFilter()
    cost__gte = django_filters.NumberFilter(field_name='cost', lookup_expr='gte')
    cost__lte = django_filters.NumberFilter(field_name='cost', lookup_expr='lte')
    album_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Album
        fields = ['cost','album_name']


class AlbumView(GenericAPIView):
    queryset = Album.approved_only.all()
    serializer_class = AlbumSerializer

    def get(self, request):
        ## Preparing Paginator
        paginator = AlbumPagination()
        filtered = AlbumFilter(request.GET, Album.approved_only.all()) ## Pass the data to a filter

        ## Displaying Paginated Data
        query = paginator.paginate_queryset(queryset=filtered.qs , request= request)
        data = AlbumSerializer(query, many=True)
        return paginator.get_paginated_response(data.data)



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


def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False



def cost__gte(val, qs):
    if isfloat(val):
        return qs.filter(cost__gte=float(val))
    else:
        raise ValidationError("cost__gte only takes Numbers.")

def cost__lte(val, qs):
    if isfloat(val):
        return qs.filter(cost__lte=float(val))
    else:
        raise ValidationError("cost__lte only takes Numbers.")

def manual_filter(queryset, params):
    if "cost__gte" in params:  ##Applying "Cost Greater Than or Equal" Filter if provided
        queryset = cost__gte(params['cost__gte'][0], queryset)

    if "cost__lte" in params:  ##Applying "Cost Less Than or Equal" Filter if provided
        queryset = cost__lte(params['cost__lte'][0], queryset)

    if "album_name" in params:  ## Applying name Filter if provided
        p = params['album_name'][0]
        queryset = queryset.filter(album_name__icontains=p)

    return queryset

class AlbumView_ManualFilters(AlbumView):
    queryset = Album.approved_only.all()
    serializer_class = AlbumSerializer

    def get(self, request):
        params = dict(request.query_params) ##Extracting Query Parameters
        queryset = Album.approved_only.all()


        queryset = manual_filter(queryset, params) ##Filtering according to Existing Filters

        ## Preparing Paginator
        paginator = AlbumPagination()

        ## Displaying Paginated Data
        query = paginator.paginate_queryset(queryset= queryset , request= request)
        data = AlbumSerializer(query, many=True)
        return paginator.get_paginated_response(data.data)


