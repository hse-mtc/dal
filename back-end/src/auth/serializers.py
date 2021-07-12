from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from conf.settings import CREATE_PASSWORD_TOKEN_LIFETIME

from auth.models import (
    Group,
    Permission,
)
from lms.functions import get_user_from_request


class PermissionSerializer(serializers.ModelSerializer):
    scope_display = serializers.CharField(source="get_scope_display")

    class Meta:
        model = Permission
        # using __all__ does not display codename
        fields = [
            "id", "method", "viewset", "scope", "scope_display", "codename",
            "name"
        ]


class PermissionListSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source="codename")
    label = serializers.CharField(source="name")

    class Meta:
        model = Permission
        fields = ["key", "label"]


class PermissionRequestSerializer(serializers.ModelSerializer):
    # specifying this as codename is a property field
    codename = serializers.CharField()

    def validate(self, attrs):
        if attrs["codename"].count(".") != 2:
            raise ValidationError(
                f"Incorrect codename template for \"{attrs['codename']}\"")

        viewset, method, scope = attrs["codename"].split(".")

        if scope.upper() not in Permission.Scope.names:
            raise ValidationError(
                f"Scope \"{scope}\" does not exist " \
                f"(permission \"{attrs['codename']}\""
            )
        scope = int(getattr(Permission.Scope, scope.upper()))

        permission = Permission.objects.filter(viewset=viewset,
                                               method=method,
                                               scope=scope)

        if not permission.exists():
            raise ValidationError(
                f"Permission \"{attrs['codename']}\" does not exist")

        return super().validate(attrs)

    class Meta:
        model = Permission
        fields = ["codename"]


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def get_permissions(self, obj) -> list[str]:
        return [perm.codename for perm in obj.permissions.all()]


class GroupListSerializer(serializers.ModelSerializer):
    key = serializers.IntegerField(source="id")
    label = serializers.CharField(source="name")

    class Meta:
        model = Group
        fields = ["key", "label"]


class GroupShortSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """Represent a list of groups as a list of strings."""
        return instance.name

    class Meta:
        model = Group
        fields = ["name"]


class GroupMutateSerializer(serializers.ModelSerializer):

    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        read_only=False,
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def update(self, instance, validated_data):
        if "name" in validated_data:
            # validate name
            if Group.objects.filter(name=validated_data["name"]).exists():
                raise serializers.ValidationError(
                    "Group with this name already exists.")
            instance.name = validated_data["name"]
            instance.save()
        if "permissions" in validated_data:
            # validate permissions
            data = [{
                "codename": perm
            } for perm in validated_data["permissions"]]
            perms_validation = PermissionRequestSerializer(data=data, many=True)
            perms_validation.is_valid(raise_exception=True)

            # get permission objects
            def get_perm_object(codename):
                viewset, method, scope = codename.split(".")
                scope = int(getattr(Permission.Scope, scope.upper()))

                return Permission.objects.get(viewset=viewset,
                                              method=method,
                                              scope=scope)

            perm_objects = [
                get_perm_object(codename)
                for codename in validated_data["permissions"]
            ]
            # delete old perms and set new ones
            instance.permissions.clear()
            instance.permissions.add(*perm_objects)
        return instance


class PersonSerialier(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    milgroups = serializers.ListField(
        child=serializers.IntegerField(),
        read_only=True,
    )
    milfaculty = serializers.CharField(read_only=True)

    class Meta:
        fields = ["id", "type", "milgroups", "milfaculty"]

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    """Display main user info and all permissions."""
    all_permissions = serializers.SerializerMethodField(read_only=True)

    person = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "all_permissions", "campuses", "person"]

    def get_all_permissions(self, obj) -> list[str]:
        return PermissionSerializer(obj.get_all_permissions(), many=True).data

    def get_person(self, obj) -> str:
        # pylint:disable=(invalid-name)
        # pylint:disable=(redefined-builtin)
        # try to find teachers
        user_type, user = get_user_from_request(obj)

        class PersonObject:

            def __init__(self, id, type, milgroups, milfaculty):
                self.id = id
                self.type = type
                self.milgroups = milgroups
                self.milfaculty = milfaculty

        milgroups = []
        milfaculty = None

        if user_type == "student":
            milgroups = [user.milgroup.milgroup]
            milfaculty = user.milgroup.milfaculty.milfaculty

        if user_type == "teacher":
            milgroups = [user.milgroup.milgroup]
            milfaculty = user.milfaculty.milfaculty

        person = PersonObject(0 if user is None else user.id, user_type,
                              milgroups, milfaculty)
        return PersonSerialier(person).data


class UserDetailedSerializer(serializers.ModelSerializer):
    """Display main user info, user permissions and groups."""
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "permissions",
            "campuses",
            "groups",
        ]

    def get_permissions(self, obj) -> list[str]:
        return [perm.codename for perm in obj.permissions.all()]


class UserDetailedMutateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        read_only=False,
        required=False,
    )
    groups = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        read_only=False,
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ["permissions", "groups"]

    def update(self, instance, validated_data):
        if "permissions" in validated_data:
            # validate permissions
            data = [{
                "codename": perm
            } for perm in validated_data["permissions"]]
            perms_validation = PermissionRequestSerializer(data=data, many=True)
            perms_validation.is_valid(raise_exception=True)

            # get permission objects
            def get_perm_object(codename):
                viewset, method, scope = codename.split(".")
                scope = int(getattr(Permission.Scope, scope.upper()))

                return Permission.objects.get(viewset=viewset,
                                              method=method,
                                              scope=scope)

            perm_objects = [
                get_perm_object(codename)
                for codename in validated_data["permissions"]
            ]
            # delete old perms and set new ones
            instance.permissions.clear()
            instance.permissions.add(*perm_objects)
        if "groups" in validated_data:
            # validate groups
            group_objects = Group.objects.filter(
                id__in=validated_data["groups"])
            if len(group_objects) != len(validated_data["groups"]):
                raise serializers.ValidationError(
                    "Some group ids do not exist.")

            # delete old groups and set new ones
            instance.groups.set(group_objects)
        return instance


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
