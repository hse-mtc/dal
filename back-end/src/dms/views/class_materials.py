import json

from rest_framework import status
from rest_framework import viewsets

from rest_framework.parsers import JSONParser, MultiPartParser, BaseParser
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
    SectionSerializer,
    TopicRetrieveSerializer,
    TopicSerializer,
)
from dms.filters import (
    SectionFilter,
    TopicFilter,
)
from dms.views.common import OrderUpdateAPIView

from common.models.subjects import Subject
from common.constants import MUTATE_ACTIONS
from common.parsers import MultiPartWithJSONParser

from auth.models import Permission
from auth.permissions import BasePermission

from lms.utils.functions import get_personnel_from_request_user
from lms.models.teachers import Teacher


class SectionPermission(BasePermission):
    permission_class = "sections"
    view_name_rus = "Разделы учебных дисциплин"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


class SectionOrderPermission(BasePermission):
    permission_class = "sections-order"
    view_name_rus = "Порядок разделов учебных дисциплин"


class TopicPermission(BasePermission):
    permission_class = "topics"
    view_name_rus = "Темы учебных дисциплин"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


class TopicOrderPermission(BasePermission):
    permission_class = "topics-order"
    view_name_rus = "Порядок тем учебных дисциплин"


class ClassMaterialPermission(BasePermission):
    permission_class = "class-materials"
    view_name_rus = "Учебно-методические материалы"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["sections"])
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    permission_classes = [SectionPermission]
    scoped_permission_class = SectionPermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = SectionFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF:
            return self.queryset.filter(subject__user=self.request.user)

        return self.queryset.none()

    def is_creation_allowed_by_scope(self, data):
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return True

        if scope == Permission.Scope.SELF:
            subject = Subject.objects.get(id=data["subject"])
            return self.request.user == subject.user
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )


@extend_schema(tags=["sections"])
class SectionOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Section.objects.all()
    permission_classes = [SectionOrderPermission]


@extend_schema(tags=["topics"])
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [TopicPermission]
    scoped_permission_class = TopicPermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = TopicFilter

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return TopicRetrieveSerializer
        return TopicSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        is_student = False
        personel = get_personnel_from_request_user(self.request.user)
        match personel:
            case Teacher():
                is_student = False
            case _:
                is_student = True
        if self.request.user.is_superuser:
            is_student = False
        kwargs["context"]["is_student"] = is_student
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF:
            return self.queryset.filter(section__subject__user=self.request.user)

        return self.queryset.none()

    def is_creation_allowed_by_scope(self, data):
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return True

        if scope == Permission.Scope.SELF:
            section = Section.objects.get(id=data["section"])
            return self.request.user == section.subject.user
        return False

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                TopicRetrieveSerializer(instance=instance).data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )


@extend_schema(tags=["topics"])
class TopicOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Topic.objects.all()
    permission_classes = [TopicOrderPermission]


@extend_schema(
    request=ClassMaterialMutateSerializerForSwagger,
    tags=["class-materials"],
)
class ClassMaterialViewSet(viewsets.ModelViewSet):
    queryset = ClassMaterial.objects.all()
    permission_classes = [ClassMaterialPermission]
    scoped_permission_class = ClassMaterialPermission

    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return ClassMaterialMutateSerializer
        return ClassMaterialSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF:
            return self.queryset.filter(topic__section__subject__user=self.request.user)

        return self.queryset.none()

    def is_creation_allowed_by_scope(self, data):
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.ALL:
            return True

        if scope == Permission.Scope.SELF:
            topic = Topic.objects.get(id=data["topic"])
            return self.request.user == topic.section.subject.user
        return False

    def create(self, request, *args, **kwargs):
        # pylint: disable=too-many-locals

        many_fields = request.data.pop("data", None)

        # request contains fields for only one object, fall back to default
        if many_fields is None:
            return super().create(request, *args, **kwargs)

        many_content = request.data.pop("content")
        many_fields_new = []
        for fields, content in zip(many_fields, many_content):
            if isinstance(fields, str):
                fields = json.loads(fields)
            fields["content"] = content
            many_fields_new.append(fields)

        serializer = self.get_serializer(data=many_fields_new, many=True)
        serializer.is_valid(raise_exception=True)
        # check scoping
        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN,
        )
