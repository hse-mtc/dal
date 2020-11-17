from rest_framework import viewsets

from rest_framework.filters import OrderingFilter
from rest_framework.parsers import JSONParser

from drf_spectacular.views import extend_schema

from dms.models.books import Book
from dms.serializers.books import (
    BookMutateSerializer,
    BookSerializer,
)
from dms.permissions import (
    IsOwner,
    ReadOnly,
)
from dms.parsers import MultiPartWithJSONParser
from dms.views.common import MUTATE_ACTIONS


@extend_schema(tags=["books"])
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [ReadOnly | IsOwner]
    filter_backends = [OrderingFilter]
    ordering_fields = ["title", "publication_year"]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return BookMutateSerializer
        return BookSerializer
