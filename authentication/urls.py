from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import Register

urlpatterns = [
     path('register', Register.as_view()),

]
