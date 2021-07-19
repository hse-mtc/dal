from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
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
from dms.mixins import QuerySetScopingByUserMixin

from auth.models import Permission
from auth.permissions import BasePermission

from common.parsers import MultiPartWithJSONParser
from common.constants import MUTATE_ACTIONS


class BookPermission(BasePermission):
    permission_class = "books"
    view_name_rus = "Книги"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


class FavoriteBookPermission(BasePermission):
    permission_class = "favorite-books"
    view_name_rus = "Любимые книги"
    scopes = [
        Permission.Scope.SELF,
    ]


@extend_schema(request=BookMutateSerializerForSwagger, tags=["books"])
class BookViewSet(QuerySetScopingByUserMixin, viewsets.ModelViewSet):
    queryset = Book.objects \
        .prefetch_related("authors", "publishers", "subjects", "file", "user") \
        .order_by("title", "id")

    permission_classes = [BookPermission]
    scoped_permission_class = BookPermission

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
    queryset = FavoriteBook.objects \
        .prefetch_related("book", "user") \
        .order_by("id")

    permission_classes = [FavoriteBookPermission]
    scoped_permission_class = FavoriteBookPermission

    filter_backends = [DjangoFilterBackend]

    filterset_class = FavoriteBookFilter

    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return FavoriteBookMutateSerializer
        return FavoriteBookSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.request.user.is_superuser:
            return queryset

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.SELF:
            return queryset

        return queryset.none()

    def is_creation_allowed_by_scope(self, data):
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.SELF:
            return self.request.user.id == data["user"]
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, pk=None, **kwargs):
        # pylint: disable=unused-argument,invalid-name,arguments-differ
        favorite = FavoriteBook.objects.filter(book__id=pk)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
