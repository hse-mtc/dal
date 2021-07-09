from django.contrib.auth import get_user_model

from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions

from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework_simplejwt import views as jwt_views

from drf_spectacular.views import extend_schema

from auth.permissions import BasePermission
from auth.models import (
    Permission,
    Group,
)
from auth.serializers import (
    UserSerializer,
    UserDetailedSerializer,
    UserDetailedMutateSerializer,
    GroupSerializer,
    GroupShortSerializer,
    GroupListSerializer,
    GroupMutateSerializer,
    PermissionRequestSerializer,
    PermissionListSerializer,
    TokenPairSerializer,
    ChangePasswordSerializer,
)

from common.constants import MUTATE_ACTIONS


class PermissionPermission(BasePermission):
    permission_class = "permissions"
    view_name_rus = "Права доступа и группы"


class PasswordPermission(BasePermission):
    permission_class = "password"
    view_name_rus = "Пароль"
    methods = ["post"]
    scopes = [Permission.Scope.SELF]


@extend_schema(tags=["permissions"])
class PermissionRetrieveView(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionListSerializer

    permission_class = [PermissionPermission]


@extend_schema(tags=["auth"])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["permissions"])
class UserControlViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()

    permission_classes = [PermissionPermission]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return UserDetailedMutateSerializer
        return UserDetailedSerializer

    @extend_schema(request=PermissionRequestSerializer)
    @action(
        detail=True,
        methods=["post"],
        url_path="permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def add_permissions(self, request: Request, pk=None) -> Response:
        """Add user permissions."""
        data = PermissionRequestSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        viewset, method, scope = data.data["codename"].split(".")
        scope = int(getattr(Permission.Scope, scope.upper()))
        user = self.get_object()

        permission = Permission.objects.get(viewset=viewset,
                                            method=method,
                                            scope=scope)
        # adding the same permission does nothing,
        # so no need to check for existing permissions
        user.permissions.add(permission)
        return Response(UserDetailedSerializer(user).data)

    @extend_schema(parameters=[PermissionRequestSerializer])
    @action(
        detail=True,
        methods=["delete"],
        url_path="permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def delete_permissions(self, request: Request, pk=None) -> Response:
        """Delete user permissions."""
        query_params = PermissionRequestSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        viewset, method, scope = query_params.data["codename"].split(".")
        scope = int(getattr(Permission.Scope, scope.upper()))
        user = self.get_object()

        permission = user.permissions.filter(viewset=viewset,
                                             method=method,
                                             scope=scope)
        if not permission.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "detail": "There is no such permission in user permissions"
                })
        permission = permission[0]
        user.permissions.remove(permission)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=GroupShortSerializer)
    @action(
        detail=True,
        methods=["post"],
        url_path="groups",
    )
    # pylint: disable=invalid-name, unused-argument
    def add_groups(self, request: Request, pk=None) -> Response:
        """Add user to groups."""
        data = GroupShortSerializer(data=request.data)
        if data.is_valid():
            # if such group exists, it violates the unique constraint
            # and, thus, is invalid. That's what we need to check.
            # If data is valid, such group does not exist -> bad request
            return Response(
                {"detail": f"Group \"{data['name']}\" does not exist."},
                status=status.HTTP_400_BAD_REQUEST)

        groupname = data.data["name"]
        user = self.get_object()

        group = Group.objects.get(name=groupname)
        # adding the same group does nothing,
        # so no need to check for existing groups
        user.groups.add(group)
        return Response(UserDetailedSerializer(user).data)

    @extend_schema(parameters=[GroupShortSerializer])
    @action(
        detail=True,
        methods=["delete"],
        url_path="groups",
    )
    # pylint: disable=invalid-name, unused-argument
    def delete_groups(self, request: Request, pk=None) -> Response:
        """Delete user from a group."""
        groupname = request.query_params["name"]
        user = self.get_object()

        group = user.groups.filter(name=groupname)
        if not group.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "There is no such group in user groups"})
        group = group[0]
        user.groups.remove(group)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=GroupShortSerializer)
    @action(
        detail=True,
        methods=["patch"],
        url_path="transfer-permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def transfer_permissions(self, request: Request, pk=None) -> Response:
        """
        Transfer group permissions to user permissions
        and delete user from group.
        """
        groupname = request.data["name"]
        user = self.get_object()

        group = user.groups.filter(name=groupname)
        if not group.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "There is no such group in user groups"})
        group = group[0]
        # add group permissions
        # adding the same permission does nothing,
        # so no need to check for existing permissions
        user.permissions.add(*group.permissions.all())
        # remove user from group
        user.groups.remove(group)
        return Response(UserDetailedSerializer(user).data)

    @action(
        detail=True,
        methods=["delete"],
        url_path="permissions/all",
    )
    # pylint: disable=invalid-name, unused-argument
    def clear_permissions(self, request: Request, pk=None) -> Response:
        """Delete all user permissions."""
        user = self.get_object()

        user.permissions.remove(*user.permissions.all())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["permissions"])
class GroupViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet,
):
    queryset = Group.objects.all()
    permission_classes = [PermissionPermission]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return GroupMutateSerializer
        return GroupSerializer

    def list(self, request, *args, **kwargs):
        serializer = GroupListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @extend_schema(request=GroupMutateSerializer)
    def create(self, request: Request) -> Response:
        # validate group name
        validation = GroupMutateSerializer(data=request.data)
        validation.is_valid(raise_exception=True)

        # validate permissions
        perms = [{
            "codename": codename
        } for codename in request.data["permissions"]]
        validation = PermissionRequestSerializer(data=perms, many=True)
        validation.is_valid(raise_exception=True)

        # create group and add permissions if everything is ok
        group = Group.objects.create(name=request.data["name"])

        permissions_lst = []
        for codename in request.data["permissions"]:
            viewset, method, scope = codename.split(".")
            scope = int(getattr(Permission.Scope, scope.upper()))
            permission = Permission.objects.get(viewset=viewset,
                                                method=method,
                                                scope=scope)
            permissions_lst.append(permission)
        group.permissions.add(*permissions_lst)

        return Response(GroupSerializer(group).data)

    @extend_schema(request=PermissionRequestSerializer)
    @action(
        detail=True,
        methods=["post"],
        url_path="permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def add_permissions(self, request: Request, pk=None) -> Response:
        """Add group permissions."""
        data = PermissionRequestSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        viewset, method, scope = data.data["codename"].split(".")
        scope = int(getattr(Permission.Scope, scope.upper()))
        group = self.get_object()

        permission = Permission.objects.get(viewset=viewset,
                                            method=method,
                                            scope=scope)
        # adding the same permission does nothing,
        # so no need to check for existing permissions
        group.permissions.add(permission)
        return Response(GroupSerializer(group).data)

    @extend_schema(parameters=[PermissionRequestSerializer])
    @action(
        detail=True,
        methods=["delete"],
        url_path="permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def delete_permissions(self, request: Request, pk=None) -> Response:
        """Delete group permissions."""
        query_params = PermissionRequestSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        viewset, method, scope = query_params.data["codename"].split(".")
        scope = int(getattr(Permission.Scope, scope.upper()))
        group = self.get_object()

        permission = group.permissions.filter(viewset=viewset,
                                              method=method,
                                              scope=scope)
        if not permission.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "detail": "There is no such permission in group permissions"
                })
        permission = permission[0]
        group.permissions.remove(permission)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["auth"])
class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [PasswordPermission]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        user = request.user
        user.set_password(password)
        user.save()
        return Response(status=HTTP_200_OK)


# ------------------------------------------------------------------------------


class TokenObtainPairView(jwt_views.TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


class TokenRefreshView(jwt_views.TokenRefreshView):
    permission_classes = [permissions.AllowAny]


TokenObtainPairExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenObtainPairView)

TokenRefreshExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenRefreshView)
