from datetime import datetime

from common.utils.populate import get_or_create

from lms.models.students import Student
from lms.models.achievements import (
    Achievement,
    AchievementType,
)


def create_achievement_types() -> dict[str, AchievementType]:
    types = [
        {
            "title": "Спортивные",
        },
        {
            "title": "Научные",
        },
    ]

    return {
        fields["title"]: get_or_create(AchievementType, **fields)
        for fields in types
    }


def create_achievements(
    achievement_types: dict[str, AchievementType],
    students: dict[str, Student],
    nearest_day: datetime,
) -> None:
    date_f = "%Y-%m-%d"

    achievements = [
        {
            "student": students["Исаков"],
            "type": achievement_types["Спортивные"],
            "text": "Мастер спорта по футболу",
        },
        {
            "student": students["Хромов"],
            "type": achievement_types["Научные"],
            "text": "Написал научную статью",
            "date": nearest_day.strftime(date_f),
        },
    ]

    for fields in achievements:
        get_or_create(Achievement, **fields)
