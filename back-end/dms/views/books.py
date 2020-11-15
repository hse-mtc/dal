from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.filters import OrderingFilter

from dms.models.books import Book
from dms.serializers.books import (
    BookSerializer,
    BookMutateSerializer,
)
from dms.permissions import (
    ReadOnly,
    IsOwner,
)
from dms.parsers import MultiPartWithJSONParser
from dms.views.common import MUTATE_ACTIONS


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
