from datetime import (
    datetime,
    timedelta,
)

from common.utils.populate import get_or_create

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.models.punishments import Punishment


def create_punishments(
    students: dict[str, Student],
    teachers: dict[str, Teacher],
    nearest_day: datetime,
) -> None:
    date_f = "%Y-%m-%d"

    punishments = [
        {
            "type": Punishment.Type.PUNISHMENT.value,
            "student": students["Хромов"],
            "teacher": teachers["Никандров"],
            "reason": "Не пришел на пары",
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "remove_date": nearest_day.strftime(date_f),
        },
        {
            "type": Punishment.Type.REBUKE.value,
            "student": students["Исаков"],
            "teacher": teachers["Репалов"],
            "reason": "Сломал парту",
            "date": nearest_day.strftime(date_f),
            "remove_date": None,
        },
    ]

    for fields in punishments:
        get_or_create(Punishment, **fields)
