from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from drf_spectacular.views import extend_schema

from django_filters.rest_framework import DjangoFilterBackend

from dms.filters import (
    BookFilter,
    FavoriteBookFilter,
)
from dms.models.books import (Book, FavoriteBook)
from dms.serializers.books import (
    BookMutateSerializer,
    BookMutateSerializerForSwagger,
    BookSerializer,
    FavoriteBookSerializer,
    FavoriteBookMutateSerializer,
)
from dms.permissions import (
    IsOwner,
    ReadOnly,
)

from common.parsers import MultiPartWithJSONParser
from common.constants import MUTATE_ACTIONS


@extend_schema(request=BookMutateSerializerForSwagger, tags=["books"])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects \
        .prefetch_related("authors", "publishers", "subjects", "file", "user") \
        .order_by("title")

    permission_classes = [ReadOnly | IsOwner]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = BookFilter
    ordering_fields = ["title", "publication_year"]
    search_fields = ["title", "annotation"]

    parser_classes = [MultiPartWithJSONParser, JSONParser]

    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return BookMutateSerializer
        return BookSerializer


@extend_schema(tags=["favorite-books"])
class FavoriteBookViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBook.objects.prefetch_related("book", "user")

    permission_classes = [ReadOnly | IsOwner]
    filter_backends = [DjangoFilterBackend]

    filterset_class = FavoriteBookFilter

    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return FavoriteBookMutateSerializer
        return FavoriteBookSerializer

    def destroy(self, request, *args, pk=None, **kwargs):
        # pylint: disable=unused-argument,invalid-name,arguments-differ
        favorite = FavoriteBook.objects.filter(book__id=pk)
        favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)
