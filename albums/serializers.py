from rest_framework import serializers
from .models import Album
from rest_framework.pagination import LimitOffsetPagination
from artists.models import Artist

class AlbumPagination(LimitOffsetPagination):  ## Album Pagination Class
    page_size = 1
    page_query_param = 'page'

class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('stage_name', 'social_media_link')


class AlbumSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):  ## Adding Help Text to the "Approved" field
        super(AlbumSerializer, self).__init__(*args, **kwargs)
        self.fields['approved'].help_text = '> Approve the album if its name is not explicit'


    artist = ArtistListSerializer(required=False)  ## Display Details of the parent Artist
    album_name = serializers.CharField(required=True)
    cost = serializers.DecimalField(max_digits=5, decimal_places=2, required=True)
    album_release_date = serializers.DateTimeField(required=True)
    approved = serializers.BooleanField(default=False)

    class Meta:
        model = Album
        fields = ('album_id', 'artist', 'album_name', 'album_release_date', 'cost', 'approved')
