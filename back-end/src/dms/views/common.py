from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from django_filters.rest_framework import DjangoFilterBackend
from dms.filters import SubjectFilter

from dms.models.common import (
    Author,
    Publisher,
)
from dms.models.papers import Paper
from dms.models.books import Book
from dms.serializers.class_materials import SubjectRetrieveSerializer
from dms.serializers.common import (
    AuthorSerializer,
    OrderUpdateSerializer,
    PublisherSerializer,
    SubjectSerializer,
)
from dms.mixins import QuerySetScopingByUserMixin

from common.models.subjects import Subject

from auth.models import Permission
from auth.permissions import BasePermission


class AuthorPermission(BasePermission):
    permission_class = "authors"
    view_name_rus = "Авторы"


@extend_schema(tags=["authors"])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AuthorPermission]


class PublisherPermission(BasePermission):
    permission_class = "publishers"
    view_name_rus = "Места публикаций"


@extend_schema(tags=["publishers"])
class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [PublisherPermission]


class SubjectPermission(BasePermission):
    permission_class = "subjects"
    view_name_rus = "Учебные дисциплины"
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["subjects"])
class SubjectViewSet(QuerySetScopingByUserMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.order_by("-title", "id")

    permission_classes = [SubjectPermission]
    scoped_permission_class = SubjectPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SubjectFilter
    search_fields = ["title", "annotation"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubjectRetrieveSerializer
        return SubjectSerializer


class OrderUpdateAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = OrderUpdateSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StatisticsPermission(BasePermission):
    permission_class = "statistics"
    view_name_rus = "Статистика"
    methods = ["get"]
    scopes = [
        Permission.Scope.SELF,
    ]


@extend_schema(tags=["statistics"],
               parameters=[
                   OpenApiParameter("start_date", OpenApiTypes.DATE,
                                    OpenApiParameter.QUERY),
                   OpenApiParameter("end_date", OpenApiTypes.DATE,
                                    OpenApiParameter.QUERY)
               ])
class StatisticsAPIView(generics.GenericAPIView):
    # pylint: disable-msg=too-many-locals
    permission_classes = [StatisticsPermission]
    scoped_permission_class = StatisticsPermission

    def get(self, request, uid):
        start_date = request.GET.get("start_date", "")
        end_date = request.GET.get("end_date", "")

        paper_filter = Paper.objects.filter(user__id=uid)
        book_filter = Book.objects.filter(user__id=uid)
        subject_filter = Subject.objects.filter(user__id=uid)

        if start_date:
            paper_filter = paper_filter.filter(upload_date__gte=start_date)
            book_filter = book_filter.filter(upload_date__gte=start_date)
        if end_date:
            paper_filter = paper_filter.filter(upload_date__lte=end_date)
            book_filter = book_filter.filter(upload_date__lte=end_date)

        data = {
            "paper_count": paper_filter.count(),
            "book_count": book_filter.count(),
            "subject_count": subject_filter.count()
        }

        return Response(data, status=status.HTTP_200_OK)
