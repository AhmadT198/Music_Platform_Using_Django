from django.urls import path, include

from artists.views import *

urlpatterns = [
    path('', artist.as_view()),


]

