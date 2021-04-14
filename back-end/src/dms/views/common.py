from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
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

from common.models.subjects import Subject


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
    queryset = Subject.objects.order_by("-title", "id")
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


@extend_schema(tags=["statistics"],
               parameters=[
                   OpenApiParameter("start_date", OpenApiTypes.DATE,
                                    OpenApiParameter.QUERY),
                   OpenApiParameter("end_date", OpenApiTypes.DATE,
                                    OpenApiParameter.QUERY)
               ])
class StatisticsAPIView(generics.GenericAPIView):
    # pylint: disable-msg=too-many-locals
    permission_classes = [permissions.AllowAny]

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

        return Response(data, status=HTTP_200_OK)
