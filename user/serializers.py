from django.db import transaction
from rest_framework import serializers

from user.models import Role, User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    role = serializers.SerializerMethodField(read_only=True)
    # role_code = serializers.CharField(write_only=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "email",
            "last_name",
            "username",
            "role",
            "password",
        ]

    def get_role(self, obj):
        try:
            return obj.user.role.name
        except:
            return None

    def create(self, validated_data):
        with transaction.atomic():
            # role_code = validated_data.pop("role_code")
            password = validated_data.pop("password")
            validated_data["role"] = Role.objects.get(id=1)
            user = User.objects.create(**validated_data)
            user.set_password(password)
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


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
