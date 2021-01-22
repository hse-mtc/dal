from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from lms.filters.mark import MarkFilter
from lms.models.mark import Mark
from lms.serializers.mark import MarkSerializer


@extend_schema(tags=['mark'])
class MarkViewSet(ModelViewSet):
    serializer_class = MarkSerializer
    queryset = Mark.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = MarkFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
