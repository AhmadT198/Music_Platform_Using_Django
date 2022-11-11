import json
import pytest
from albums.serializers import *
from albums.models import Album
from albums.serializers import AlbumSerializer
from django.core import serializers
from artists.models import Artist
from rest_framework.response import Response
from users.models import User


@pytest.mark.django_db
def test_album_serializer_serialize():
    ar = Artist.objects.create(stage_name="testArt")
    al = Album.approved_only.create(artist_id=ar.artist_id,album_name="ass", cost=19.99,approved=True)
    album = Album.approved_only.all()
    actual = dict(list(AlbumSerializer(album, many=True).data)[0])
    actual['artist'] = dict(actual['artist'])
    expected = {
        'album_id' : al.album_id,
        'artist' : {
            'stage_name' : ar.stage_name,
            'social_media_link': ar.social_media_link
        },
        'album_name' : al.album_name,
        'album_release_date' : str(str(al.album_release_date).replace('+00:00','Z')).replace(' ','T'),
        'cost' : str(al.cost),
        'approved' : al.approved
    }

    print(actual)
    assert actual == expected


@pytest.mark.django_db
def test_album_serializer_deserialize():
    data = { ## Album Instance in Dict
        'album_name' : "testalbum",
        'album_release_date' : "2022-11-11T00:00:00Z",
        'cost' :19.99,
        'approved' : True
    }

    ##Calling Serializer
    ser = AlbumSerializer(data=data)
    ser.is_valid() ## Validating Data

    ##Adjusting Data types
    data['cost'] = str(data['cost'])
    ser.data['album_release_date'] = str(ser.data['album_release_date']).replace('+00:00','Z').replace(' ','T')

    assert ser.data == data


