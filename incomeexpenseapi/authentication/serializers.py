# import re
# from django.db.models import fields
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
# import pdb

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should contain alphanumeric characters")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, min_length=6,write_only=True)
    email = serializers.EmailField()

    class Meta:
        model= User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        # pdb.set_trace()
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if user.is_active is False:
            raise AuthenticationFailed("Account disabled")
        if not user.is_verified:
            raise AuthenticationFailed("Account not verified, please confirm your email")

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

