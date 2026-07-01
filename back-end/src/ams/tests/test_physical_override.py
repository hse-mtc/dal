# pylint: disable=redefined-outer-name,invalid-name
"""Тесты ручной (дословной) загрузки физ. результатов комиссии.

Ключевой инвариант: при override `secondary_score` и агрегаты пишутся дословно
и НЕ перетираются калькулятором (scoring.py), а обычный CRUD по-прежнему
пересчитывает баллы автоматически.
"""
import pytest

from ams.models.applicants import ApplicationProcess
from ams.models.physical import ExerciseResult
from ams.physical.exercises import ExerciseType
from ams.utils.export.comp_sel_protocol import _format_exercise_value

OVERRIDE_URL = "/api/ams/applicants/{pk}/exercise-results/override/"


# ---------------------------------------------------------------------------
# Уровень модели: механизм _skip_recalc
# ---------------------------------------------------------------------------


@pytest.mark.django_db
class TestRecalcBypass:
    def test_normal_save_recalculates(self, application_process):
        """Обычное сохранение пересчитывает балл из value (строгий scoring)."""
        er = ExerciseResult.objects.create(
            application_process=application_process,
            exercise_type=ExerciseType.SPEED_RUN_60M,
            value=8.33,
        )
        er.refresh_from_db()
        application_process.refresh_from_db()
        # 8.33 по строгой логике DAL -> 87
        assert er.secondary_score == 87
        assert application_process.speed_score == 87

    def test_skip_recalc_keeps_verbatim_score(self, application_process):
        """С _skip_recalc дословный secondary_score не перетирается."""
        er = ExerciseResult(
            application_process=application_process,
            exercise_type=ExerciseType.SPEED_RUN_60M,
            value=8.33,
            secondary_score=90,
        )
        er._skip_recalc = True
        er.save()
        er.refresh_from_db()
        application_process.refresh_from_db()
        assert er.secondary_score == 90  # НЕ 87
        # агрегаты сохранения не трогает
        assert application_process.speed_score == 0

    def test_skip_recalc_on_delete(self, application_process):
        """Удаление с _skip_recalc не запускает пересчёт агрегатов."""
        er = ExerciseResult(
            application_process=application_process,
            exercise_type=ExerciseType.SPEED_RUN_60M,
            value=8.3,
            secondary_score=90,
        )
        er._skip_recalc = True
        er.save()

        application_process.speed_score = 55  # sentinel
        application_process.save(update_fields=["speed_score"])

        er._skip_recalc = True
        er.delete()

        application_process.refresh_from_db()
        assert application_process.speed_score == 55  # не пересчитан в 0

    def test_normal_delete_recalculates(self, application_process):
        """Обычное удаление пересчитывает агрегаты."""
        er = ExerciseResult.objects.create(
            application_process=application_process,
            exercise_type=ExerciseType.SPEED_RUN_60M,
            value=8.3,
        )
        application_process.refresh_from_db()
        assert application_process.speed_score == 90

        er.delete()  # без _skip_recalc
        application_process.refresh_from_db()
        assert application_process.speed_score == 0


# ---------------------------------------------------------------------------
# Форматирование результата в протоколе (мм:сс для длинных дистанций)
# ---------------------------------------------------------------------------


def test_format_value_mmss_for_long_runs():
    assert _format_exercise_value(3.85, ExerciseType.LONG_RUN_1KM) == "3:51"
    assert _format_exercise_value(12.5, ExerciseType.LONG_RUN_3KM) == "12:30"
    # спринт — как есть, десятичные секунды
    assert _format_exercise_value(8.33, ExerciseType.SPEED_RUN_60M) == 8.33
    # счётные — целое
    assert _format_exercise_value(21.0, ExerciseType.PULL_UPS) == 21


# ---------------------------------------------------------------------------
# Эндпоинт override
# ---------------------------------------------------------------------------

OVERRIDE_BODY = {
    "results": [
        {"exercise_type": "PULL_UPS", "value": 21, "secondary_score": 83},
        {"exercise_type": "RUN_60", "value": 8.33, "secondary_score": 90},
        {"exercise_type": "RUN_1K", "value": 3.85, "secondary_score": 39},
    ],
    "strength_score": 83,
    "speed_score": 90,
    "endurance_score": 39,
    "physical_test_grade": 100,
}


@pytest.mark.django_db
def test_override_endpoint_stores_verbatim(su_client, applicant):
    resp = su_client.post(
        OVERRIDE_URL.format(pk=applicant.id),
        OVERRIDE_BODY,
        content_type="application/json",
    )
    assert resp.status_code == 200

    ap = applicant.application_process
    ap.refresh_from_db()
    assert ap.physical_test_grade == 100
    assert (ap.strength_score, ap.speed_score, ap.endurance_score) == (83, 90, 39)

    results = {e.exercise_type: e for e in ap.exercise_results.all()}
    # RUN_60: балл дословный (90), НЕ строгий scoring (87)
    assert results["RUN_60"].secondary_score == 90
    assert results["RUN_60"].value == 8.33
    assert results["RUN_1K"].secondary_score == 39


@pytest.mark.django_db
def test_override_replaces_stale_results(su_client, applicant):
    ap = applicant.application_process
    # заранее кладём «старое» упражнение, которого нет в новом наборе
    stale = ExerciseResult(
        application_process=ap,
        exercise_type=ExerciseType.LONG_RUN_3KM,
        value=13.0,
        secondary_score=55,
    )
    stale._skip_recalc = True
    stale.save()

    resp = su_client.post(
        OVERRIDE_URL.format(pk=applicant.id),
        OVERRIDE_BODY,
        content_type="application/json",
    )
    assert resp.status_code == 200

    types = set(ap.exercise_results.values_list("exercise_type", flat=True))
    assert types == {"PULL_UPS", "RUN_60", "RUN_1K"}  # RUN_3K удалён


@pytest.mark.django_db
def test_override_forbidden_without_permission(test_client, applicant):
    resp = test_client.post(
        OVERRIDE_URL.format(pk=applicant.id),
        OVERRIDE_BODY,
        content_type="application/json",
    )
    assert resp.status_code == 403
