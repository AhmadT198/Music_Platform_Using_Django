from django.urls import path, include

from albums.views import album

urlpatterns = [
    path('', album.as_view())

]

