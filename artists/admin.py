from django.contrib import admin
from artists.models import Artist
from artists.forms import ArtistForm


# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    form = ArtistForm
    list_display = ['stage_name', 'social_media_link', 'approved_albums_count']

    def approved_albums_count(self, obj):
        return obj.albums.filter(approved=True).count()
