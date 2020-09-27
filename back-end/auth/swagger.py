from drf_yasg.openapi import (
    IN_HEADER,
    TYPE_STRING,
    Parameter,
)

token_auth_header = Parameter(
    "Authorization",
    IN_HEADER,
    type=TYPE_STRING,
    required=True,
    default="Token ",
)
