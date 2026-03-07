from auth.permissions import BasePermission, Permission
from drf_spectacular.views import extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ams.models.applicants import Applicant
from ams.models.physical import ExerciseResult
from ams.physical.exercises import get_exercise_registry
from ams.serializers.physical import (
    ExerciseDefinitionSerializer,
    ExerciseResultSerializer,
)


class ExerciseResultPermission(BasePermission):
    permission_class = "exercise_results"
    view_name_rus = "Результаты упражнений"
    methods = ["get", "post", "patch", "delete"]
    scopes = [Permission.Scope.ALL, Permission.Scope.SELF]


@extend_schema(tags=["physical"])
class ExerciseListView(APIView):
    """GET /ams/physical/exercises/ — справочник упражнений."""

    def get(self, request: Request) -> Response:
        registry = get_exercise_registry()
        data = ExerciseDefinitionSerializer(registry.values(), many=True).data
        return Response(data)


@extend_schema(tags=["physical"])
class ExerciseResultViewSet(ModelViewSet):
    """CRUD результатов упражнений для конкретного абитуриента.

    URL: /ams/applicants/{applicant_pk}/exercise-results/
    """

    serializer_class = ExerciseResultSerializer
    permission_classes = [ExerciseResultPermission]
    lookup_field = "exercise_type"

    def get_queryset(self):
        applicant_pk = self.kwargs["applicant_pk"]
        return ExerciseResult.objects.filter(
            application_process__applicant__id=applicant_pk
        )

    def _get_application_process(self):
        applicant_pk = self.kwargs["applicant_pk"]
        applicant = Applicant.objects.get(pk=applicant_pk)
        return applicant.application_process

    def perform_create(self, serializer):
        ap = self._get_application_process()
        serializer.save(application_process=ap)
        # Пересчет происходит автоматически в ExerciseResult.save()

    def perform_update(self, serializer):
        serializer.save()
        # Пересчет происходит автоматически в ExerciseResult.save()

    def perform_destroy(self, instance):
        instance.delete()
        # Пересчет происходит автоматически в post_delete сигнале
