from rest_framework import generics
from rest_framework import viewsets

from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from django_filters.rest_framework import DjangoFilterBackend

from taggit.models import Tag

from drf_spectacular.views import extend_schema
from rest_framework import pagination

from auth.permissions import BasePermission

from dms.models.papers import (
    Category,
    Paper,
)
from dms.serializers.papers import (
    CategorySerializer,
    PaperMutateSerializer,
    PaperMutateSerializerForSwagger,
    PaperSerializer,
    TagSerializer,
)

from dms.filters import PaperFilter

from common.parsers import MultiPartWithJSONParser
from common.constants import MUTATE_ACTIONS


class CategoryPermission(BasePermission):
    permission_class = "categories"
    view_name_rus = "Категории статей"


@extend_schema(tags=["categories"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission]

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        if Paper.objects.filter(category=category).exists():
            return Response(
                {"message": "Category has documents and can not be deleted."},
                status=HTTP_422_UNPROCESSABLE_ENTITY)

        return super().destroy(request, *args, **kwargs)


class PapersPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


class TagPermission(BasePermission):
    permission_class = "tags"
    view_name_rus = "Ключевые слова статей"
    methods = ["get"]


@extend_schema(tags=["tags"])
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagPermission]


class PaperPermission(BasePermission):
    permission_class = "papers"
    view_name_rus = "Статьи"


@extend_schema(request=PaperMutateSerializerForSwagger, tags=["papers"])
class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects \
        .prefetch_related("authors", "category", "publishers", "file", "tags") \
        .order_by("-publication_date", "title", "id")

    permission_classes = [PaperPermission]
    scoped_permission_class = PaperPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PaperFilter
    search_fields = ["title", "annotation", "tags__name"]

    # parser_classes = [MultiPartWithJSONParser, JSONParser]

    pagination_class = PapersPageNumberPagination

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return PaperMutateSerializer
        return PaperSerializer
