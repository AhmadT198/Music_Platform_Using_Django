from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class artist(APIView):
    def get(self, request): ## Unauthenticated Users can view the artists freely
        print(request.user)
        data = ArtistSerializer(Artist.objects.all(), many=True)
        return Response(data.data, status= status.HTTP_200_OK)
    def post(self, request):
        if (request.user.is_authenticated): ## Only Authenticated Users can Add Artists
            try:

                ## Pass the data to the ArtistSerializer
                data = ArtistSerializer(data=request.data)

                if data.is_valid(): ## if it is Valid
                    data.save() ## Save and return the new data
                    return Response(data.data,status.HTTP_200_OK)
                return Response(data.errors, status=status.HTTP_406_NOT_ACCEPTABLE) ## if not valid, return the errors
            except Exception as e:
                return Response({"message" :str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else: ## ELse, if not authenticated
            return Response({"message": "Please log in"}, status=status.HTTP_403_FORBIDDEN)


