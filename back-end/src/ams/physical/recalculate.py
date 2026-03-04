"""
Пересчёт баллов по физической подготовке.

Вызывается при каждом создании/обновлении/удалении ExerciseResult.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from ams.physical.exercises import Direction, get_exercise_registry
from ams.physical.scoring import (
    compute_direction_score,
    compute_global_score,
)

if TYPE_CHECKING:
    from ams.models.applicants import ApplicationProcess


def _get_applicant_age(application_process: ApplicationProcess) -> int:
    """Возраст абитуриента на текущую дату (полных лет)."""
    try:
        birth_date: date = application_process.applicant.birth_info.date
    except Exception:
        return 0
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def recalculate_physical_scores(application_process: ApplicationProcess) -> None:
    """Пересчитать все баллы физ. подготовки для ApplicationProcess.

    1. Обновляет secondary_score на каждом ExerciseResult.
    2. Вычисляет баллы по направлениям (max).
    3. Вычисляет глобальный балл (physical_test_grade).
    4. Сохраняет изменения.
    """
    registry = get_exercise_registry()
    age = _get_applicant_age(application_process)

    results = list(application_process.exercise_results.all())

    # Пересчитываем secondary_score для каждого результата
    for result in results:
        definition = registry.get(result.exercise_type)
        if definition is None:
            continue
        result.secondary_score = definition.convert(
            result.value, result.extra_params, age
        )
        result.save(update_fields=["secondary_score"])

    # Группируем по направлениям
    direction_scores: dict[str, list[int]] = {d.value: [] for d in Direction}
    for result in results:
        definition = registry.get(result.exercise_type)
        if definition is None:
            continue
        direction_scores[definition.direction].append(result.secondary_score)

    strength = compute_direction_score(direction_scores[Direction.STRENGTH])
    speed = compute_direction_score(direction_scores[Direction.SPEED])
    endurance = compute_direction_score(direction_scores[Direction.ENDURANCE])

    application_process.strength_score = strength
    application_process.speed_score = speed
    application_process.endurance_score = endurance
    application_process.physical_test_grade = compute_global_score(
        strength, speed, endurance, age
    )
    application_process.save(
        update_fields=[
            "strength_score",
            "speed_score",
            "endurance_score",
            "physical_test_grade",
        ]
    )
