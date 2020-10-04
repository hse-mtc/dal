from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema

from auth.swagger import token_auth_header


@swagger_auto_schema(method="GET", manual_parameters=[token_auth_header])
@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def info(request: Request) -> Response:
    data = {
        "roles": ["admin"],
        "avatar": "mock",
        "name": "Mock M. M.",
    }

    return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def logout(request: Request) -> Response:
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response({"message": "User logged out successfully."},
                    status=HTTP_200_OK)
