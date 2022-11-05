from django.contrib import admin
from django import forms
from .models import *
from .forms import *


## To Allow Song creation from Album creation form.
class SongTabular(admin.TabularInline):
    model = Song
    formset = BaseSongFormSet ## Pass the provided Songs to this FormSet

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    inlines = [SongTabular]
    readonly_fields = ('created','modified')



# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)