from datetime import datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
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

from lms.filters.marks import MarkFilter

from lms.models.common import Milgroup
from lms.models.marks import Mark
from lms.models.students import Student
from lms.models.lessons import Lesson

from lms.serializers.common import MilgroupSerializer
from lms.serializers.subjects import LessonSubjectSerializer
from lms.serializers.lessons import LessonSerializer
from lms.serializers.marks import (
    MarkSerializer,
    MarkMutateSerializer,
    MarkJournalSerializer,
    MarkJournalQuerySerializer,
)
from lms.views.archived_viewset import ArchivedModelViewSet

from auth.permissions import BasePermission


class MarkPermission(BasePermission):
    permission_class = 'auth.mark'


@extend_schema(tags=['marks'])
class MarkViewSet(ArchivedModelViewSet):
    queryset = Mark.objects.all()

    permission_classes = [MarkPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = MarkFilter
    search_fields = ['student__surname', 'student__name', 'student__patronymic']

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return MarkMutateSerializer
        return MarkSerializer

    # override POST - new mark
    # pylint: disable=W1113
    # pylint: disable=W0221
    def create(self, request, *args, **kwargs):
        request.data['mark'] = [request.data['mark']]
        return super().create(request, *args, **kwargs)

    # override PUT - add mark to array
    # pylint: disable=W1113
    # pylint: disable=W0221
    def update(self, request, pk=None, *args, **kwargs):
        request.data['mark'] = self.queryset.get(
            id=pk).mark + [request.data['mark']]
        return super().update(request, pk, *args, **kwargs)

    # override PATCH - change last mark in array
    # pylint: disable=W1113
    # pylint: disable=W0221
    def partial_update(self, request, pk=None, *args, **kwargs):
        tmp = request.data['mark']
        request.data['mark'] = self.queryset.get(id=pk).mark
        request.data['mark'][-1] = tmp
        return super().update(request, pk, partial=True, *args, **kwargs)

    # override DELETE - delete last mark in array
    # pylint: disable=W1113
    # pylint: disable=W0221
    def destroy(self, request, pk=None, *args, **kwargs):
        request.data['mark'] = self.queryset.get(id=pk).mark
        request.data['mark'].pop(-1)
        if len(request.data['mark']) == 0:
            return super().destroy(request, pk, *args, **kwargs)
        return super().update(request, pk, *args, **kwargs)


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

        # date_range = get_date_range(date_from, date_to, milgroup['weekday'])
        lessons = Lesson.objects.filter(
            date__lte=date_to,
            date__gte=date_from,
            milgroup=request.query_params['milgroup'],
            subject=request.query_params['subject']).order_by(
                'date', 'ordinal')
        data['lessons'] = LessonSerializer(lessons, many=True).data
        date_range = list({item.date for item in lessons})

        # add dates and absences
        data['dates'] = sorted(date_range)
        data['students'] = MarkJournalSerializer(Student.objects.filter(
            milgroup__milgroup=request.query_params['milgroup']),
                                                 context={
                                                     'request': request,
                                                     'date_range': date_range,
                                                     'subject': subject_query.id
                                                 },
                                                 many=True).data

        return Response(data, status=HTTP_200_OK)
