from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from conf.settings import CREATE_PASSWORD_TOKEN_LIFETIME

from auth.models import (
    Group,
    Permission,
)


class PermissionSerializer(serializers.ModelSerializer):
    scope_display = serializers.CharField(source="get_scope_display")

    class Meta:
        model = Permission
        # using __all__ does not display codename
        fields = [
            "id", "method", "viewset", "scope", "scope_display", "codename",
            "name"
        ]


class PermissionRequestSerializer(serializers.ModelSerializer):
    # specifying this as codename is a property field
    codename = serializers.CharField()

    class Meta:
        model = Permission
        fields = ["codename"]


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "permissions", "campuses"]

    def get_permissions(self, obj) -> list[str]:
        return PermissionSerializer(obj.get_all_permissions(), many=True).data


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CreatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CreatePasswordTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token = token.access_token
        token.set_exp(lifetime=CREATE_PASSWORD_TOKEN_LIFETIME)
        return token

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
