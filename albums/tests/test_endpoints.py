import json
import pytest
from albums.serializers import *
from albums.models import Album
from albums.serializers import AlbumSerializer
from django.core import serializers
from artists.models import Artist
from rest_framework.response import Response
from users.models import User
from rest_framework.test import APIClient




@pytest.mark.django_db
def test_get_auth(auth_client):
    '''

    ## Testing Get Request for the endpoint '/albums/' from Authenticated users

    '''

    ##Creating Dummy Data
    ar = Artist.objects.create(stage_name="testArt")
    al = Album.approved_only.create(artist_id=ar.artist_id,album_name="ass", cost=19.99,approved=True)

    ## Creating Authenticated client
    user = User.objects.create_user(username='ahmadt198', password='password')
    client = auth_client(user=user)

    ##Sending Request
    response= client.get('/albums/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_unauth(auth_client):
    '''

    ## Testing Get Request for the endpoint '/albums/' from UnAuthenticated users

    '''

    ##Creating Dummy Data
    ar = Artist.objects.create(stage_name="testArt")
    al = Album.approved_only.create(artist_id=ar.artist_id, album_name="ass", cost=19.99, approved=True)

    ## Creating UnAuthenticated client
    client =APIClient()

    ##Sending Request
    response = client.get('/albums/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_auth(auth_client):
    '''

        ## Testing POST Request for the endpoint '/albums/' from Authenticated users

    '''

    data = {  ## Album Instance in Dict
        'album_name': "testalbum",
        'album_release_date': "2022-11-11T00:00:00Z",
        'cost': 19.99,
        'approved': True
    }

    ##Creating Artist User
    user = User.objects.create_user(username='ahmadt198', password='password')
    ar = Artist.objects.create(stage_name="testArt",user=user)
    client = auth_client(user=user)

    ## Sending Request
    response= client.post('/albums/',data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_unauth(auth_client):
    '''

            ## Testing POST Request for the endpoint '/albums/' from UnAuthenticated users

        '''
    data = {  ## Album Instance in Dict
        'album_name': "testalbum",
        'album_release_date': "2022-11-11T00:00:00Z",
        'cost': 19.99,
        'approved': True
    }
    ##Creating Unauthenticated client
    client = APIClient()

    ##Sending Request
    response = client.post('/albums/', data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_post_unauth(auth_client):
    data = {  ## Album Instance in Dict
        'album_id' : 1,
        'album_name': "testalbum",
        'album_release_date': "2022-11-11T00:00:00Z",
        'cost': 19.99,
        'approved': True,
        'artist' : None

    }

    ## Creating Dummy Data
    user = User.objects.create_user(username='ahmadt198', password='password')
    ar = Artist.objects.create(stage_name="testArt", user=user)
    al = Album.approved_only.create( album_name="testalbum",
                                    cost=19.99, approved=True,album_release_date="2022-11-11T00:00:00Z")


    ## Sending Request
    client = auth_client(user=user)
    response = client.get('/albums/')

    ## Adjusting Formats and data types
    formated_response = dict((dict(response.data)['results'])[0])
    data['cost'] = str(data['cost'])

    assert formated_response == data