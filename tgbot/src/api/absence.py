import typing as tp
import operator

from dataclasses import dataclass

import asyncio
from aiohttp import ClientResponse

from api.client import client

from api.student import Student, State


def create_body(student: Student) -> dict:
    return {
        'student': {
            'id': student.id
        },
        'absence_type': student.absence_type,
        'absence_status': student.absence_status,
    }


def absence_statistic(students: list[Student]) -> str:
    absent_students = [i for i in students if i.state == State.absent]
    text = f'''
Список студентов отправлен!

По списку: {len(students)}
Налицо: {len(students) - len(absent_students)}
Отсутствуют: {len(absent_students)}

ФИО отсутствующих студентов:
'''
    for student in sorted(absent_students,
                          key=operator.attrgetter('full_name')):
        text = '\n'.join([text, student.full_name])
    return text


async def post_absence(students: list[Student]) -> str:
    absent_students = [
        student for student in students
        if student.state.value == State.absent.value
    ]
    tasks = []
    for student in absent_students:
        body = create_body(student)
        tasks.append(client.post('lms/absence/', json=body))
    await asyncio.gather(*tasks)
    return absence_statistic(students)
