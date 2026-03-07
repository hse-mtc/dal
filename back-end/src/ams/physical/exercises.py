from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from django.db import models


class Direction(models.TextChoices):
    STRENGTH = "ST", "Сила"
    SPEED = "SP", "Быстрота"
    ENDURANCE = "EN", "Выносливость"


class ExerciseType(models.TextChoices):
    # Сила
    PULL_UPS = "PULL_UPS", "Подтягивание на перекладине"
    LIFT_TURNOVER = "LIFT_TURNOVER", "Подъем переворотом на перекладине"
    LIFT_FORCE = "LIFT_FORCE", "Подъем силой на перекладине"
    KETTLEBELL_SNATCH = "KETTLEBELL_SNATCH", "Рывок гири"

    # Быстрота
    SPEED_RUN_60M = "RUN_60", "Бег на 60 м"
    SPEED_RUN_100M = "RUN_100", "Бег на 100 м"
    SHUTTLE_RUN = "SHUTTLE_RUN", "Челночный бег 10×10 м"

    # Выносливость
    LONG_RUN_1KM = "RUN_1K", "Бег на 1 км"
    LONG_RUN_3KM = "RUN_3K", "Бег на 3 км"


@dataclass
class ExerciseDefinition:
    exercise_type: str
    name: str
    direction: str
    unit: str
    convert: Callable[[float, dict, int], int]
    higher_is_better: bool = True
    extra_params: list[str] = field(default_factory=list)


def _build_registry() -> dict[str, ExerciseDefinition]:
    from ams.physical.scoring import (
        convert_pull_ups,
        convert_lift_turnover,
        convert_lift_force,
        convert_kettlebell_snatch,
        convert_run_60m,
        convert_run_100m,
        convert_shuttle_run,
        convert_run_1km,
        convert_run_3km,
    )

    return {
        # Сила
        ExerciseType.PULL_UPS: ExerciseDefinition(
            exercise_type=ExerciseType.PULL_UPS,
            name="Подтягивание на перекладине",
            direction=Direction.STRENGTH,
            unit="раз",
            higher_is_better=True,
            convert=convert_pull_ups,
        ),
        ExerciseType.LIFT_TURNOVER: ExerciseDefinition(
            exercise_type=ExerciseType.LIFT_TURNOVER,
            name="Подъем переворотом на перекладине",
            direction=Direction.STRENGTH,
            unit="раз",
            higher_is_better=True,
            convert=convert_lift_turnover,
        ),
        ExerciseType.LIFT_FORCE: ExerciseDefinition(
            exercise_type=ExerciseType.LIFT_FORCE,
            name="Подъем силой на перекладине",
            direction=Direction.STRENGTH,
            unit="раз",
            higher_is_better=True,
            convert=convert_lift_force,
        ),
        ExerciseType.KETTLEBELL_SNATCH: ExerciseDefinition(
            exercise_type=ExerciseType.KETTLEBELL_SNATCH,
            name="Рывок гири",
            direction=Direction.STRENGTH,
            unit="раз",
            higher_is_better=True,
            convert=convert_kettlebell_snatch,
            extra_params=["weight"],  # Вес спортсмена в кг
        ),
        # Быстрота
        ExerciseType.SPEED_RUN_60M: ExerciseDefinition(
            exercise_type=ExerciseType.SPEED_RUN_60M,
            name="Бег на 60 м",
            direction=Direction.SPEED,
            unit="сек",
            higher_is_better=False,
            convert=convert_run_60m,
        ),
        ExerciseType.SPEED_RUN_100M: ExerciseDefinition(
            exercise_type=ExerciseType.SPEED_RUN_100M,
            name="Бег на 100 м",
            direction=Direction.SPEED,
            unit="сек",
            higher_is_better=False,
            convert=convert_run_100m,
        ),
        ExerciseType.SHUTTLE_RUN: ExerciseDefinition(
            exercise_type=ExerciseType.SHUTTLE_RUN,
            name="Челночный бег 10×10 м",
            direction=Direction.SPEED,
            unit="сек",
            higher_is_better=False,
            convert=convert_shuttle_run,
        ),
        # Выносливость
        ExerciseType.LONG_RUN_1KM: ExerciseDefinition(
            exercise_type=ExerciseType.LONG_RUN_1KM,
            name="Бег на 1 км",
            direction=Direction.ENDURANCE,
            unit="мин",
            higher_is_better=False,
            convert=convert_run_1km,
        ),
        ExerciseType.LONG_RUN_3KM: ExerciseDefinition(
            exercise_type=ExerciseType.LONG_RUN_3KM,
            name="Бег на 3 км",
            direction=Direction.ENDURANCE,
            unit="мин",
            higher_is_better=False,
            convert=convert_run_3km,
        ),
    }


_registry: dict[str, ExerciseDefinition] | None = None


def get_exercise_registry() -> dict[str, ExerciseDefinition]:
    global _registry
    if _registry is None:
        _registry = _build_registry()
    return _registry
