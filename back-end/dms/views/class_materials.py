from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status

from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from dms.models.class_materials import (
    Section,
    Topic,
    ClassMaterial,
)
from dms.serializers.class_materials import (
    SectionSerializer,
    SectionRetrieveSerializer,
    TopicSerializer,
    TopicRetrieveSerializer,
    ClassMaterialSerializer,
    ClassMaterialMutateSerializer,
)
from dms.permissions import (
    IsOwner,
    ReadOnly,
)
from dms.parsers import MultiPartWithJSONParser
from dms.views.common import (
    OrderUpdateAPIView,
    MUTATE_ACTIONS,
)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SectionRetrieveSerializer
        return SectionSerializer


class SectionOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Section.objects.all()


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TopicRetrieveSerializer
        return TopicSerializer


class TopicOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Topic.objects.all()


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

        many_fields = request.data.pop("data")
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
