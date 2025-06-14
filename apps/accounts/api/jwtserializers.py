from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # خیلی مهم

    def validate(self, attrs):
        credentials = {
            'email': attrs.get("email"),
            'password': attrs.get("password")
        }

        user = authenticate(email=credentials['email'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError('Invalid email or password')

        data = super().validate({
            'email': credentials['email'],  # چون داخل parent serializer هنوز username می‌خواهد
            'password': credentials['password'],
        })

        return data
