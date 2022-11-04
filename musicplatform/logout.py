from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout




class Logout(View):

    def get(self, request):
        try:
            logout(request)
            print("logged Out")
            return JsonResponse({"message" : "Success"})
        except:
            return JsonResponse({"message" : "failedd to log out"})
