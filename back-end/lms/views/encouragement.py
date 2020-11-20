from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.encouragement import Encouragement
from lms.serializers.encouragement import EncouragementSerializer
from lms.filters.encouragement import EncouragementFilterSet


@extend_schema(tags=['encouragement'])
class EncouragementViewSet(ModelViewSet):
    serializer_class = EncouragementSerializer
    queryset = Encouragement.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilterSet
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
