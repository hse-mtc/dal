from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.models import Profile
from conf.settings import CREATE_PASSWORD_TOKEN_LIFETIME


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["name", "codename"]


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "groups"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    def get_permissions(self, obj):
        user_perms = Permission.objects.filter(group__user=obj.user.id)
        return user_perms.values_list("codename", flat=True)

    class Meta:
        model = Profile
        exclude = ["id"]


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
