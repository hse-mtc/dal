from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from lms.models.encouragement import Encouragement
from lms.serializers.encouragement import EncouragementSerializer
from lms.filters.encouragement import EncouragementFilter

from auth.permissions import BasicPermission


class EncouragementPermission(BasicPermission):
    permission_class = 'auth.encouragement'


@extend_schema(tags=['encouragement'])
class EncouragementViewSet(ModelViewSet):
    serializer_class = EncouragementSerializer
    queryset = Encouragement.objects.all()

    permission_classes = [EncouragementPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = EncouragementFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']
