import typing as tp
import asyncio
import operator

from api.client import client
from api.student import (
    Student,
    State,
)


def absence_statistic(students: list[Student]) -> str:
    absent_students = [s for s in students if s.state == State.ABSENT]
    absent_students.sort(key=operator.attrgetter("fullname"))

    text = f"""
Список студентов отправлен.

По списку: {len(students)}
Налицо: {len(students) - len(absent_students)}
Отсутствуют: {len(absent_students)}
"""

    # Someone is missing.
    if len(absent_students) > 0:
        text += "\nФИО отсутствующих студентов:\n"
        text += "\n".join([s.fullname for s in absent_students])

    return text


async def post_absence(students: list[Student], *args: tp.Any,
                       **kwargs: tp.Any) -> str:
    absent_students = [
        student for student in students
        if student.state.value == State.ABSENT.value
    ]

    pending_responses = [
        client.post(
            "lms/absences/",
            json=student.to_body(),
            *args,
            **kwargs,
        ) for student in absent_students
    ]
    await asyncio.gather(*pending_responses)

    return absence_statistic(students)
