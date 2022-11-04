from django.contrib import admin
from django import forms
from albums.models import Album
from albums.forms import AlbumForm

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm

    readonly_fields = ('created','modified')



# Register your models here.
admin.site.register(Album, AlbumAdmin)
