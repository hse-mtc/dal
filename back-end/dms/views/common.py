from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from rest_framework.filters import SearchFilter

from drf_spectacular.views import extend_schema

from django_filters.rest_framework import DjangoFilterBackend
from dms.filters import SubjectFilter

from dms.models.common import (
    Author,
    Publisher,
)
from dms.serializers.class_materials import SubjectRetrieveSerializer
from dms.serializers.common import (
    AuthorSerializer,
    OrderUpdateSerializer,
    PublisherSerializer,
    SubjectSerializer,
)

from common.models.subjects import Subject

MUTATE_ACTIONS = ["create", "update", "partial_update"]


@extend_schema(tags=["authors"])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["publishers"])
class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["subjects"])
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SubjectFilter
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
