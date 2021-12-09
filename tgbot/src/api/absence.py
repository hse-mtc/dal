import asyncio
import operator
import textwrap
import typing as tp

from datetime import datetime

from api.client import client
from api.student import (
    Student,
    State,
)


def absence_statistic(
    milgroup_title: str,
    students: list[Student],
    absent_students: list[Student],
) -> str:
    text = textwrap.dedent(f"""
        Список студентов отправлен\\.
        
        ```
              Взвод: {milgroup_title}
          По списку: {len(students)}
             Налицо: {len(students) - len(absent_students)}
        Отсутствуют: {len(absent_students)}
        ```
    """)

    if absent_students:
        absent_students.sort(key=operator.attrgetter("fullname"))
        text += "\nОтсутствующие студенты:\n"
        text += "\n".join([f"\\- {s.fullname}" for s in absent_students])

    return text


async def fetch_today_absences(milgroup: int) -> list[dict]:
    today = datetime.now().strftime("%Y-%m-%d")
    response = await client.get(
        f"lms/absences/",
        params={
            "milgroup": milgroup,
            "date_from": today,
            "date_to": today,
        },
    )
    return await response.json()


async def post_absence(
    students: list[Student],
    *args: tp.Any,
    **kwargs: tp.Any,
) -> str:
    absences = await fetch_today_absences(students[0].milgroup.id)

    if absences:
        pending_responses = [
            client.delete(f"lms/absences/{absence['id']}/")
            for absence in absences
        ]
        await asyncio.gather(*pending_responses)

    absent_students = [
        student for student in students
        if student.state.value == State.ABSENT.value
    ]

    if absent_students:
        pending_responses = [
            client.post("lms/absences/", json=student.to_body(), *args, **kwargs)
            for student in absent_students
        ]
        await asyncio.gather(*pending_responses)

    return absence_statistic(
        milgroup_title=students[0].milgroup.title,
        students=students,
        absent_students=absent_students,
    )
