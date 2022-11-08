from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, MinimumLengthValidator, \
    CommonPasswordValidator, NumericPasswordValidator, validate_password
from .models import *
from users.models import User



class UserSerializer(serializers.ModelSerializer):


    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data): ## Overriding the Validate method for Password Validation
        if data.get("password1",None) != data.get("password2",None):
            raise ValidationError("Passwords do not match.")
        else:
            validate_password(data.get("password1",None))
        return data


    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
