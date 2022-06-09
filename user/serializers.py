from django.db import transaction
from rest_framework import serializers

from user.models import Role, User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    password_confirm = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "address",
            "phone",
            "password",
            "password_confirm",
            "role"
        ]

    def get_role(self, obj):
        try:
            return obj.user.role.name
        except:
            return None

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            password_confirm = validated_data.pop("password_confirm")
            user = User.objects.create(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
            return user


class InputSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
    token = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["code", "error", "name", "email", "token"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]