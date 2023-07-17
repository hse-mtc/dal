from auth.models import User
from common.utils.populate import get_or_create

from lms.models.lessons import Lesson
from lms.models.students import Student
from lms.models.marks import Mark


def create_marks(
    lessons: list[Lesson], students: dict[str, Student], user_to_create_marks: User
) -> None:
    marks = [
        {
            "values": [5],
            "lesson": lessons[0],
            "student": students["Хромов"],
            "changed_by": user_to_create_marks,
        },
        {
            "values": [4],
            "lesson": lessons[0],
            "student": students["Исаков"],
            "changed_by": user_to_create_marks,
        },
        {
            "values": [3],
            "lesson": lessons[0],
            "student": students["Кацевалов"],
            "changed_by": user_to_create_marks,
        },
        {
            "values": [5],
            "lesson": lessons[1],
            "student": students["Хромов"],
            "changed_by": user_to_create_marks,
        },
        {
            "values": [3],
            "lesson": lessons[1],
            "student": students["Исаков"],
            "changed_by": user_to_create_marks,
        },
        {
            "values": [2],
            "lesson": lessons[1],
            "student": students["Кацевалов"],
            "changed_by": user_to_create_marks,
        },
    ]

    for fields in marks:
        get_or_create(Mark, **fields)
