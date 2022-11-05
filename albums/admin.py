from django.contrib import admin
from django import forms
from .models import *
from .forms import AlbumForm
class SongTabular(admin.TabularInline):
    model = Song

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    inlines = [SongTabular]
    readonly_fields = ('created','modified')



# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)