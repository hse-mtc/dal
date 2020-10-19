from drf_yasg2.openapi import (
    IN_HEADER,
    TYPE_STRING,
    Parameter,
)

from conf.settings import SIMPLE_JWT

token_auth_header = Parameter(
    "Authorization",
    IN_HEADER,
    type=TYPE_STRING,
    required=True,
    default=SIMPLE_JWT["AUTH_HEADER_TYPES"][0] + " ",
)
