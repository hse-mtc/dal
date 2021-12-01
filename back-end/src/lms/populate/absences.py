from datetime import (
    datetime,
    time,
    timedelta,
)

from common.utils.populate import get_or_create

from lms.models.students import Student
from lms.models.absences import (
    Absence,
    AbsenceTime
)


def create_absences(
    students: dict[str, Student],
    nearest_day: datetime,
) -> None:
    date_f = "%Y-%m-%d"

    absences = [
        {
            "excuse": Absence.Excuse.LEGITIMATE.value,
            "status": Absence.Status.CLOSED.value,
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "reason": "Заболел",
            "attachment": None,
            "comment": "Болеть будет недолго",
            "student": students["Кацевалов"],
        },
        {
            "excuse": Absence.Excuse.LATE.value,
            "status": Absence.Status.CLOSED.value,
            "date": nearest_day.strftime(date_f),
            "reason": "Электричка опоздала",
            "attachment": None,
            "comment": "",
            "student": students["Хромов"],
        },
        {
            "excuse": Absence.Excuse.ILLEGITIMATE.value,
            "status": Absence.Status.OPEN,
            "date": (nearest_day - timedelta(14)).strftime(date_f),
            "reason": "Прогул",
            "attachment": None,
            "comment": "Лежал дома на диване",
            "student": students["Хромов"],
        },
    ]

    for fields in absences:
        _ = get_or_create(Absence, **fields)


def create_absence_restriction_time() -> AbsenceTime:
    if not AbsenceTime.objects.exists():
        # TODO(TmLev): Maybe extract this default time to `settings`?
        restriction_time = time(hour=9, minute=15)
        AbsenceTime.objects.create(absence_restriction_time=restriction_time)

    return AbsenceTime.objects.all().first()
