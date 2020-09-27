from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import (
    IN_HEADER,
    TYPE_STRING,
    Parameter,
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        Parameter(
            "Authorization",
            IN_HEADER,
            type=TYPE_STRING,
            required=True,
            default="Token ",
        ),
    ],
)
@csrf_exempt
@api_view(["GET"])
def info(request: Request) -> Response:
    data = {
        "roles": ["admin"],
        "avatar": request.user.profile.photo,
        "name": request.user.profile.name,
    }

    return Response(data, status=HTTP_200_OK)
