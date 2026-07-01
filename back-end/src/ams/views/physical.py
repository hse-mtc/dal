from auth.permissions import BasePermission, Permission
from django.db import transaction
from drf_spectacular.views import extend_schema
from rest_framework import status
from rest_framework.decorators import action
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
    PhysicalOverrideSerializer,
)


class ExerciseResultPermission(BasePermission):
    permission_class = "exercise_results"
    view_name_rus = "Результаты упражнений"
    methods = ["get", "post", "patch", "delete"]
    scopes = [Permission.Scope.ALL, Permission.Scope.SELF]


class ExerciseResultOverridePermission(BasePermission):
    permission_class = "exercise_results_override"
    view_name_rus = "Ручной ввод результатов упражнений"
    methods = ["post"]
    # Только ALL: абитуриент не может задать себе балл комиссии дословно.
    scopes = [Permission.Scope.ALL]


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

    @extend_schema(request=PhysicalOverrideSerializer, responses={200: None})
    @action(
        detail=False,
        methods=["post"],
        url_path="override",
        permission_classes=[ExerciseResultOverridePermission],
    )
    def override(self, request: Request, applicant_pk=None) -> Response:
        """Дословная загрузка физ. результатов комиссии БЕЗ пересчёта баллов.

        Полностью заменяет набор результатов абитуриента: `value` и
        `secondary_score` пишутся как есть, агрегаты выставляются напрямую.
        Идемпотентно — повторный POST с тем же телом даёт то же состояние.
        """
        # pylint: disable=unused-argument
        serializer = PhysicalOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        ap = self._get_application_process()
        incoming = {item["exercise_type"]: item for item in data["results"]}

        with transaction.atomic():
            # Удаляем устаревшие результаты (пересчёт подавляем).
            for stale in ap.exercise_results.exclude(exercise_type__in=incoming.keys()):
                stale._skip_recalc = True
                stale.delete()

            # Апсертим переданные — дословно, без пересчёта.
            # ВАЖНО: `_skip_recalc` ставим ДО первого save() (в т.ч. на создании),
            # иначе пересчёт при вставке затрёт secondary_score других упражнений.
            for etype, item in incoming.items():
                obj = ap.exercise_results.filter(exercise_type=etype).first()
                if obj is None:
                    obj = ExerciseResult(application_process=ap, exercise_type=etype)
                obj.value = item["value"]
                obj.secondary_score = item["secondary_score"]
                obj.extra_params = item.get("extra_params", {})
                obj._skip_recalc = True
                obj.save()

            # Агрегаты — напрямую.
            ap.strength_score = data["strength_score"]
            ap.speed_score = data["speed_score"]
            ap.endurance_score = data["endurance_score"]
            ap.physical_test_grade = data["physical_test_grade"]
            ap.save(
                update_fields=[
                    "strength_score",
                    "speed_score",
                    "endurance_score",
                    "physical_test_grade",
                ]
            )

        return Response(status=status.HTTP_200_OK)
