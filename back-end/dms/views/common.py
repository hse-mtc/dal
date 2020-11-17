from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from rest_framework.filters import SearchFilter

from dms.models.common import (
    Author,
    Publisher,
    Subject,
)
from dms.serializers.class_materials import SubjectRetrieveSerializer
from dms.serializers.common import (
    AuthorSerializer,
    OrderUpdateSerializer,
    PublisherSerializer,
    SubjectSerializer,
)

MUTATE_ACTIONS = ["create", "update", "partial_update"]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ["title", "annotation"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubjectRetrieveSerializer
        return SubjectSerializer


class OrderUpdateAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderUpdateSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
