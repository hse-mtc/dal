from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.views import extend_schema

from auth.models import Permission
from auth.permissions import BasePermission

from common.constants import MUTATE_ACTIONS
from common.parsers import MultiPartWithJSONParser
from dms.mixins import QuerySetScopingByUserMixin
from dms.models.videos import Video
from dms.serializers.videos import (
    VideoMutateSerializer,
    VideoMutateSerializerForSwagger,
    VideoSerializer,
)


class VideoPermission(BasePermission):
    permission_class = "videos"
    view_name_rus = "Видео"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


@extend_schema(request=VideoMutateSerializerForSwagger, tags=["videos"])
class VideoViewSet(QuerySetScopingByUserMixin, viewsets.ModelViewSet):
    queryset = Video.objects.select_related("file", "user").order_by(
        "-upload_date", "id"
    )

    permission_classes = [VideoPermission]
    scoped_permission_class = VideoPermission

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["title", "upload_date"]
    search_fields = ["title", "annotation", "file__name"]

    parser_classes = [MultiPartWithJSONParser, JSONParser]

    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return VideoMutateSerializer
        return VideoSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )
        if scope == Permission.Scope.ALL:
            return self.queryset.all()

        if scope == Permission.Scope.SELF:
            return self.queryset.filter(user=self.request.user)

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
            return self.request.user.id == data["user"]
        return False

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
