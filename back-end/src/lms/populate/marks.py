from common.utils.populate import get_or_create

from lms.models.lessons import Lesson
from lms.models.students import Student
from lms.models.marks import Mark


def create_marks(
    lessons: list[Lesson],
    students: dict[str, Student],
) -> None:
    marks = [
        {
            "values": [5],
            "lesson": lessons[0],
            "student": students["Хромов"],
        },
        {
            "values": [4],
            "lesson": lessons[0],
            "student": students["Исаков"],
        },
        {
            "values": [3],
            "lesson": lessons[0],
            "student": students["Кацевалов"],
        },
        {
            "values": [5],
            "lesson": lessons[1],
            "student": students["Хромов"],
        },
        {
            "values": [3],
            "lesson": lessons[1],
            "student": students["Исаков"],
        },
        {
            "values": [2],
            "lesson": lessons[1],
            "student": students["Кацевалов"],
        },
    ]

    for fields in marks:
        get_or_create(Mark, **fields)
