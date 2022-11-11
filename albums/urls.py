from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AlbumView.as_view())

]

