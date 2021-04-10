from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from rest_framework import permissions
from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import extend_schema

from auth.serializers import (UserSerializer, TokenPairSerializer,
                              CreatePasswordSerializer,
                              CreatePasswordTokenSerializer,
                              ChangePasswordSerializer, PermissionSerializer,
                              UserPermissionSerializerForSwagger)


@extend_schema(tags=["auth"])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


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


@extend_schema(tags=["permissions"])
class AllPermissionView(ListAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["permissions"], request=UserPermissionSerializerForSwagger)
class UserPermissionView(APIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "user"

    def get(self, request, user):
        user_permissions = self.queryset.filter(user=user)
        serializer = self.serializer_class(user_permissions, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request, user):
        user = get_user_model().objects.get(id=user)
        user.user_permissions.set(request.data["permissions_id"])
        user.save()
        return Response(HTTP_200_OK)


# ------------------------------------------------------------------------------

TokenObtainPairExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenObtainPairView)

TokenRefreshExtendedView = extend_schema(
    responses={200: TokenPairSerializer},
    tags=["auth"],
)(TokenRefreshView)
