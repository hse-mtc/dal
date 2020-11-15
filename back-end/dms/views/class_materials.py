from rest_framework import viewsets
from rest_framework import permissions

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
