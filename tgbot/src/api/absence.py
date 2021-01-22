import typing as tp

from dataclasses import dataclass

import asyncio
from aiohttp import ClientResponse

from api.client import client

from .student import Student


def create_body(student: Student) -> dict:
    return {
        'student': {
            'id': student.id
        },
        'absence_type': student.absence_type,
        'absence_status': student.absence_status,        
    }


def absence_statistic(students: list[Student]) -> str:
    absent_students = [i for i in students if not bool(int(i.state))]
    text = f'''
Список студентов отправлен!

По списку: {len(students)}
Налицо: {len(students) - len(absent_students)}
Отсутствуют: {len(absent_students)}

ФИО отсутствующих студентов:
'''
    for student in absent_students:
        text = '\n'.join([text, student.full_name])
    return text


async def post_one_absence(student: Student) -> dict:
    body = create_body(student)
    async with client.post(f'lms/absence/', json=body) as response:
        data: dict[str, tp.Any] = await response.json()
    return data


async def post_all_absence(students: list[Student]) -> bool:
    results = await asyncio.gather(
        *[post_one_absence(student) for student in students
          if not bool(int(student.state))],
        return_exceptions=True)
    return absence_statistic(students)
