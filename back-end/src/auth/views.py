from django.contrib.auth import get_user_model

from rest_framework import permissions, viewsets
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

from auth.models import Permission

from auth.serializers import (
    UserSerializer,
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


@extend_schema(tags=["auth"])
class UserControlViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    permission_classes = []

    @extend_schema(request=PermissionRequestSerializer)
    @action(
        detail=True,
        methods=["post"],
        url_path="permissions",
    )
    # pylint: disable=invalid-name, unused-argument
    def post_permissions(self, request: Request, pk=None) -> Response:
        """Add user permissions."""
        data = PermissionRequestSerializer(data=request.data)
        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        viewset, method, scope = request.data["codename"].split(".")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        user = self.get_object()

        permission = Permission.objects.filter(viewset=viewset,
                                               method=method,
                                               scope=scope)
        if permission.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data="There is no such permission")
        permission = permission[0]
        # adding the same permission does nothing,
        # so no need to check for existing permissions
        user.permissions.add(permission)
        return Response(status=status.HTTP_200_OK, data="Ok")

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

        viewset, method, scope = request.query_params["codename"].split(".")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        user = self.get_object()

        permission = user.permissions.filter(viewset=viewset,
                                             method=method,
                                             scope=scope)
        if permission.count() == 0:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="There is no such permission in user permissions")
        permission = permission[0]
        user.permissions.remove(permission)
        return Response(status=status.HTTP_200_OK, data="Ok")


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
