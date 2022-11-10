from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, \
    CommonPasswordValidator, NumericPasswordValidator, validate_password
from .models import *
from users.models import User



class RegisterSerializer(serializers.ModelSerializer):


    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data): ## Overriding the Validate method for Password Validation
        u = data.get("username",None)
        if len(User.objects.filter(username=u)) != 0:
            raise ValidationError("Username taken.")

        if data.get("password1",None) != data.get("password2",None):
            raise ValidationError("Passwords do not match.")
        else:
            validate_password(data.get("password1",None))
        return data

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password1'])
        return user

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']



class loginSerializer(serializers.ModelSerializer):


    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


    class Meta:
        model = User
        fields = ['username', 'password']
