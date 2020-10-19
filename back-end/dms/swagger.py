from drf_yasg2.openapi import (
    Items,
    Parameter,
    IN_QUERY,
    TYPE_ARRAY,
    TYPE_INTEGER,
)

author_array = Parameter(
    name="authors",
    in_=IN_QUERY,
    type=TYPE_ARRAY,
    items=Items(type=TYPE_INTEGER),
    collection_format="multi",
)
