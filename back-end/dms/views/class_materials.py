from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from dms.models.class_materials import (
    ClassMaterial,
    Section,
    Topic,
)
from dms.serializers.class_materials import (
    ClassMaterialMutateSerializer,
    ClassMaterialMutateSerializerForSwagger,
    ClassMaterialSerializer,
    SectionRetrieveSerializer,
    SectionSerializer,
    TopicRetrieveSerializer,
    TopicSerializer,
)
from dms.permissions import (
    IsOwner,
    ReadOnly,
)
from dms.filters import SectionFilter
from dms.parsers import MultiPartWithJSONParser
from dms.views.common import (
    OrderUpdateAPIView,)
from common.constants import MUTATE_ACTIONS


@extend_schema(tags=["sections"])
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SectionFilter
    search_fields = ["topics__title", "topics__class_materials__title"]

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return SectionRetrieveSerializer
        return SectionSerializer


@extend_schema(tags=["sections"])
class SectionOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Section.objects.all()


@extend_schema(tags=["topics"])
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TopicRetrieveSerializer
        return TopicSerializer


@extend_schema(tags=["topics"])
class TopicOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Topic.objects.all()


@extend_schema(
    request=ClassMaterialMutateSerializerForSwagger,
    tags=["class-materials"],
)
class ClassMaterialViewSet(viewsets.ModelViewSet):
    queryset = ClassMaterial.objects.all()
    permission_classes = [ReadOnly | IsOwner]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return ClassMaterialMutateSerializer
        return ClassMaterialSerializer

    def create(self, request, *args, **kwargs):
        # pylint: disable=too-many-locals

        many_fields = request.data.pop("data", None)

        # request contains fields for only one object, fall back to default
        if many_fields is None:
            return super().create(request, *args, **kwargs)

        many_content = request.data.pop("content")
        for fields, content in zip(many_fields, many_content):
            fields["content"] = content

        serializer = self.get_serializer(data=many_fields, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
