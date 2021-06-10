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

from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.views import extend_schema

from auth.models import Permission

from auth.serializers import (
    UserSerializer,
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
class UserControlViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    permission_classes = []

    @extend_schema(parameters=[
        OpenApiParameter(name="permission",
                         description="Permission code",
                         required=True,
                         type=str),
    ])
    @action(detail=True, methods=["post", "delete"])
    def permissions(self, request: Request) -> Response:
        """
        Modify user permissions
        """
        if "permission" not in request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        viewset, method, scope = request.query_params["permission"].split(".")
        scope = int(getattr(Permission.Scopes, scope.upper()))
        user = self.get_object()

        if request.method == "POST":
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

        # request.method == "DELETE":
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
