from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
     path('register', Register.as_view()),
     path('user/<int:pk>', UserAPI.as_view()),
     path('login', Login.as_view(), name='knox-login'),
     path('logout', Logout.as_view(), name='knox-logout'),
     path('logoutall', LogoutAll.as_view(), name='knox-logoutall')

]
