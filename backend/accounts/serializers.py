from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered")

        # Django still needs username → derive it safely
        username = email.split("@")[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        user = authenticate(
            username=user.username,  # internal only
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs
