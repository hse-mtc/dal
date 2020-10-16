from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

from drf_yasg2.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from taggit.models import Tag

from dms.filters import PaperFilter
from dms.swagger import author_array
from dms.serializers import (
    AuthorSerializer,
    BookSerializer,
    BookCreateUpdateSerializer,
    CategorySerializer,
    PaperSerializer,
    PaperCreateUpdateSerializer,
    PublisherSerializer,
    TagSerializer,
    SectionSerializer,
    SubjectSerializer,
    SubjectRetrieveSerializer,
    TopicSerializer,
)
from dms.models import (
    Author,
    Book,
    Paper,
    Publisher,
    Section,
    Subject,
    Topic,
    Category,
)
from dms.permissions import (
    IsOwner
)

class AuthorViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Author model."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Category model."""

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


class PublisherViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Publisher model."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


class SubjectViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Subject model."""

    queryset = Subject.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubjectRetrieveSerializer
        return SubjectSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SectionSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TopicSerializer


class TagListAPIView(ListAPIView):
    """List all tags."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(manual_parameters=[author_array]))
class PaperViewSet(viewsets.ModelViewSet):
    """API for CRUD operations on Paper model."""

    queryset = Paper.objects.order_by("-publication_date")
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PaperFilter
    search_fields = ["title", "annotation", "tags__name"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PaperCreateUpdateSerializer
        return PaperSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsOwner]
    filter_backends = [OrderingFilter]
    ordering_fields = ["title", "publication_year"]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return BookCreateUpdateSerializer
        return BookSerializer
