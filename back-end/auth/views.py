from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from drf_yasg.utils import swagger_auto_schema

from auth.swagger import TOKEN_AUTH_HEADER
from auth.models import Profile
from auth.serializers import ProfileSerializer


@csrf_exempt
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def info(request: Request) -> Response:
    data = {
        "roles": ["admin"],
        "avatar": "mock",
        "name": "Mock M. M.",
    }

    return Response(data, status=HTTP_200_OK)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(manual_parameters=[TOKEN_AUTH_HEADER]))
class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj
