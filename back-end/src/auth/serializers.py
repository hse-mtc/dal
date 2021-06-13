from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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

    def validate(self, attrs):
        if attrs["codename"].count(".") != 2:
            raise ValidationError(f"Incorrect codename template for \"{attrs['codename']}\"")

        viewset, method, scope = attrs["codename"].split(".")
        
        if scope.upper() not in Permission.Scopes.names:
            raise ValidationError(f"Scope \"{scope}\" does not exist (permission \"{attrs['codename']}\"")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        
        permission = Permission.objects.filter(viewset=viewset, method=method, scope=scope)

        if permission.count() == 0:
            raise ValidationError(f"Permission \"{attrs['codename']}\" does not exist")
            
        return super().validate(attrs)

    class Meta:
        model = Permission
        fields = ["codename"]


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class GroupShortSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """Represent a list of groups as a list of strings."""
        return instance.name

    class Meta:
        model = Group
        fields = ["name"]


class GroupModifySerializer(serializers.ModelSerializer):

    class StringListField(serializers.ListField):
        child = serializers.CharField()

    permissions = StringListField()

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class UserSerializer(serializers.ModelSerializer):
    """Display main user info and all permissions."""
    all_permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "all_permissions", "campuses"]

    def get_all_permissions(self, obj) -> list[str]:
        return PermissionSerializer(obj.get_all_permissions(), many=True).data


class UserDetailedSerializer(serializers.ModelSerializer):
    """Display main user info, user permissions and groups."""
    permissions = PermissionSerializer(many=True)
    groups = GroupShortSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "permissions", "campuses", "groups"]


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
