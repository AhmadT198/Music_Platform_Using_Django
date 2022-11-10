from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import *
from users.models import User



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data): ## Overriding the Validate method for Password Validation

        ## Checking the Uniqueness of the Username
        u = data.get("username",None)
        if len(User.objects.filter(username=u)) != 0:
            raise ValidationError("Username taken.")

        ## Validating the password
        if data.get("password1",None) != data.get("password2",None):
            raise ValidationError("Passwords do not match.")
        else:
            validate_password(data.get("password1",None))
        return data

    def create(self, validated_data): ## Creating the user
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password1'])
        return user

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']



class loginSerializer(serializers.ModelSerializer):
    ''' Serializer for Logging in'''

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateSerializer(serializers.ModelSerializer):
    ''' Serializer for updating User data'''

    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    bio = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio']


class PatchSerializer(serializers.ModelSerializer):
    ''' Serializer for Patching User data'''

    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio']