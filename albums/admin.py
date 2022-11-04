from django.contrib import admin
from django import forms
from albums.models import Album
from albums.forms import AlbumForm

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm

    # list_display = ['date_created']
    readonly_fields = ('date_created',)



# Register your models here.
admin.site.register(Album, AlbumAdmin)
