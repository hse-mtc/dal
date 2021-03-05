from datetime import datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from common.models.subjects import Subject
from common.constants import MUTATE_ACTIONS

from lms.filters.mark import MarkFilter

from lms.models.common import Milgroup
from lms.models.marks import Mark
from lms.models.students import Student

from lms.serializers.common import MilgroupSerializer
from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.marks import (MarkSerializer, MarkMutateSerializer,
                                  MarkJournalSerializer,
                                  MarkJournalQuerySerializer)

from lms.functions import get_date_range

from auth.permissions import BasicPermission


class MarkPermission(BasicPermission):
    permission_class = 'auth.mark'


@extend_schema(tags=['mark'])
class MarkViewSet(ModelViewSet):
    queryset = Mark.objects.all()

    permission_classes = [MarkPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = MarkFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return MarkMutateSerializer
        return MarkSerializer


@extend_schema(tags=['mark-journal'],
               parameters=[
                   OpenApiParameter(name='milgroup',
                                    description='Filter by milgroup',
                                    required=True,
                                    type=int),
                   OpenApiParameter(name='subject',
                                    description='Filter by subject',
                                    required=True,
                                    type=int),
                   OpenApiParameter(name='date_from',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
                   OpenApiParameter(name='date_to',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
               ])
class MarkJournalView(GenericAPIView):
    permission_classes = [MarkPermission]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = MarkJournalQuerySerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=HTTP_400_BAD_REQUEST)

        # final json
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(
            Milgroup.objects.get(
                milgroup=request.query_params['milgroup'])).data
        data['milgroup'] = milgroup

        subject_query = Subject.objects.get(id=request.query_params['subject'])
        subject = LessonSubjectSerializer(subject_query).data
        data['subject'] = subject

        # calculate dates
        date_from = datetime.fromisoformat(query_params.data['date_from'])
        date_to = datetime.fromisoformat(query_params.data['date_to'])

        date_range = get_date_range(date_from, date_to, milgroup['weekday'])

        # add dates and absences
        data['dates'] = date_range
        data['students'] = MarkJournalSerializer(Student.objects.filter(
            milgroup__milgroup=request.query_params['milgroup']),
                                                context={
                                                    'request': request,
                                                    'date_range': date_range,
                                                    'subject': subject_query.id
                                                },
                                                many=True).data

        return Response(data, status=HTTP_200_OK)
