from django.contrib.auth import get_user_model

from rest_framework import mixins, permissions, viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import extend_schema

from auth.models import Permission, Group

from auth.serializers import (
    UserSerializer,
    UserDetailedSerializer,
    GroupSerializer,
    GroupShortSerializer,
    GroupModifySerializer,
    PermissionRequestSerializer,
    TokenPairSerializer,
    ChangePasswordSerializer,
)


@extend_schema(tags=["auth"])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["permissions"])
class UserControlViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailedSerializer

    permission_classes = []

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
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        viewset, method, scope = data.data["codename"].split(".")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        user = self.get_object()

        permission = Permission.objects.get(viewset=viewset,
                                               method=method,
                                               scope=scope)
        # adding the same permission does nothing,
        # so no need to check for existing permissions
        user.permissions.add(permission)
        return Response(status=status.HTTP_200_OK)

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
        if not query_params.is_valid():
            return Response(query_params.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        viewset, method, scope = query_params.data["codename"].split(".")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        user = self.get_object()

        permission = user.permissions.filter(viewset=viewset,
                                             method=method,
                                             scope=scope)
        if permission.count() == 0:
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
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        groupname = data.data["name"]
        user = self.get_object()

        group = Group.objects.get(name=groupname)
        # adding the same group does nothing,
        # so no need to check for existing groups
        user.groups.add(group)
        return Response(status=status.HTTP_200_OK)

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
        if group.count() == 0:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "There is no such group in user groups"})
        group = group[0]
        user.groups.remove(group)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["permissions"])
class GroupViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = []

    @extend_schema(request=GroupModifySerializer)
    def create(self, request: Request) -> Response:
        # validate group name
        data = GroupModifySerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        # validate permissions
        perms = [{"codename": codename} for codename in data.data["permissions"]]
        validation = PermissionRequestSerializer(data=perms, many=True)
        if not validation.is_valid():
            return Response(validation.errors, status.HTTP_400_BAD_REQUEST)

        # create group and add permissions if everything is ok
        group = Group.objects.create(name=data.data["name"])

        for codename in data.data["permissions"]:
            viewset, method, scope = codename.split(".")
            scope = int(getattr(Permission.Scopes, scope.upper()))
            permission = Permission.objects.get(viewset=viewset,
                                                method=method,
                                                scope=scope)
            group.permissions.add(permission)

        return Response(GroupSerializer(group).data)


@extend_schema(tags=["auth"])
class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        user = request.user
        user.set_password(password)
        user.save()
        return Response(status=HTTP_200_OK)


# ------------------------------------------------------------------------------

TokenObtainPairExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenObtainPairView)

TokenRefreshExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenRefreshView)
