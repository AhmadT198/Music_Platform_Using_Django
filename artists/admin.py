from django.contrib import admin
from artists.models import Artist
from artists.forms import ArtistForm
from albums.models import Album


# Register your models here.
class AlbumTabular(admin.TabularInline):
    model = Album

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    form = ArtistForm
    list_display = ['stage_name', 'social_media_link', 'approved_albums_count']
    inlines = [AlbumTabular]
    def approved_albums_count(self, obj):
        return obj.albums.filter(approved=True).count()
