from datetime import timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from auth.models import Profile


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
        user_perms = Permission.objects.filter(
            group__user=obj.user.id).values_list("codename", flat=True)
        return user_perms

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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token = token.access_token
        token.set_exp(lifetime=timedelta(minutes=5))
        return token

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
