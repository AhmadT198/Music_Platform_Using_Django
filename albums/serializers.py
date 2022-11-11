from rest_framework import serializers
from albums.models import Album
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from artists.serializers import ArtistSerializer


class AlbumPagination(LimitOffsetPagination):  ## Album Pagination Class
    page_size = 2
    page_query_param = 'page'


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()  ## Display Details of the parent Artist

    def __init__(self, *args, **kwargs):  ## Adding Help Text to the "Approved" field
        super(AlbumSerializer, self).__init__(*args, **kwargs)
        self.fields['approved'].help_text = '> Approve the album if its name is not explicit'

    class Meta:
        model = Album
        fields = ('album_id', 'artist', 'album_name', 'album_release_date', 'cost', 'approved')
