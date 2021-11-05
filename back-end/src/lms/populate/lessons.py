from datetime import (
    datetime,
    timedelta,
)

from common.models.subjects import Subject

from common.utils.populate import get_or_create

from lms.models.common import Milgroup
from lms.models.teachers import Teacher
from lms.models.lessons import (
    Room,
    Lesson,
)


def create_rooms() -> dict[str, Room]:
    rooms = [
        {
            "title": "510",
        }, {
            "title": "Плац",
        }, {
            "title": "501",
        }, {
            "title": "502",
        }, {
            "title": "503",
        }, {
            "title": "504",
        }
    ]

    return {
        fields["title"]: get_or_create(Room, **fields)
        for fields in rooms
    }


def create_lessons(
    subjects: list[Subject],
    rooms: dict[str, Room],
    milgroups: dict[str, Milgroup],
    teachers: dict[str, Teacher],
    nearest_day: datetime,
) -> list[Lesson]:
    # TODO(TmLev): Link teachers too.

    subjects = {
        subject.title: subject
        for subject in subjects
    }

    date_f = "%Y-%m-%d"

    lessons = [
        {
            "type": Lesson.Type.LECTURE.value,
            "subject": subjects["Тактическая подготовка"],
            "room": rooms["510"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 1,
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "subject": subjects["Строевая подготовка"],
            "room": rooms["Плац"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 2,
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "subject": subjects["Военная топография"],
            "room": rooms["504"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 3,
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "subject": subjects["Строевая подготовка"],
            "room": rooms["Плац"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 1,
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "subject": subjects["Военная топография"],
            "room": rooms["504"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 2,
        },
        {
            "type": Lesson.Type.LECTURE.value,
            "subject": subjects["Тактическая подготовка"],
            "room": rooms["510"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 3,
        },
        {
            "type": Lesson.Type.LECTURE.value,
            "subject": subjects["Тактическая подготовка"],
            "room": rooms["510"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 1,
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "subject": subjects["Строевая подготовка"],
            "room": rooms["Плац"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 2,
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "subject": subjects["Военная топография"],
            "room": rooms["504"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 3,
        },
    ]

    return [
        get_or_create(Lesson, **fields)
        for fields in lessons
    ]
