from datetime import (
    datetime,
    timedelta,
)

from common.utils.populate import get_or_create

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.encouragements import Encouragement


def create_encouragements(
    students: dict[str, Student],
    teachers: dict[str, Teacher],
    nearest_day: datetime,
) -> None:
    date_f = "%Y-%m-%d"

    encouragements = [
        {
            "student": students["Хромов"],
            "reason": "За спортивные достижения",
            "type": Encouragement.Type.ENCOURAGEMENT.value,
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "teacher": teachers["Никандров"],
        },
        {
            "student": students["Исаков"],
            "reason": "За выступление на празднике",
            "type": Encouragement.Type.REMOVE_PUNISHMENT.value,
            "date": nearest_day.strftime(date_f),
            "teacher": teachers["Репалов"],
        },
    ]

    for fields in encouragements:
        get_or_create(Encouragement, **fields)
