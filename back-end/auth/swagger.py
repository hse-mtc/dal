from drf_yasg.openapi import (
    IN_HEADER,
    TYPE_STRING,
    Parameter,
)

from conf.settings import SIMPLE_JWT

TOKEN_AUTH_HEADER = Parameter(
    "Authorization",
    IN_HEADER,
    type=TYPE_STRING,
    required=True,
    default=SIMPLE_JWT["AUTH_HEADER_TYPES"][0] + " ",
)
