from django.urls import path, include
from .views import *

urlpatterns = [
    path('', album.as_view())

]

