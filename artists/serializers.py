from rest_framework import serializers
from .models import *



class ArtistSerializer(serializers.ModelSerializer):

    stage_name = serializers.CharField(required=True)
    social_media_link = serializers.CharField(required=True)

    def validate_stage_name(self,name): ##Check if the stage_name is Unique
        if(len(Artist.objects.filter(stage_name=name)) != 0):
            raise serializers.ValidationError("This Stage name was inserted before.")
        
    class Meta:
        model = Artist
        fields = '__all__'
