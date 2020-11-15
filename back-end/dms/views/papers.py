from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from django_filters.rest_framework import DjangoFilterBackend

from taggit.models import Tag

from dms.models.papers import (
    Category,
    Paper,
)
from dms.serializers.papers import (
    CategorySerializer,
    PaperSerializer,
    PaperMutateSerializer,
    TagSerializer,
)
from dms.permissions import (
    ReadOnly,
    IsOwner,
)
from dms.filters import PaperFilter
from dms.parsers import MultiPartWithJSONParser
from dms.views.common import MUTATE_ACTIONS


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        if Paper.objects.filter(category=category).exists():
            return Response(
                {"message": "Category has documents and can not be deleted."},
                status=HTTP_422_UNPROCESSABLE_ENTITY)

        return super().destroy(request, *args, **kwargs)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.order_by("-publication_date", "title")
    permission_classes = [ReadOnly | IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PaperFilter
    search_fields = ["title", "annotation", "tags__name"]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return PaperMutateSerializer
        return PaperSerializer
