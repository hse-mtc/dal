import typing as tp

from collections import namedtuple
from dataclasses import dataclass

from aiohttp import ClientResponse

from api.client import client


@dataclass
class Student:
    id: int
    full_name: str
    state: int = 1
    absence_type: str = 'Неуважительная'
    absence_status: str = 'Открыт'


async def fetch_students(milgroup: str) -> list[Student]:
    students = []
    async with client.get(f'lms/student?milgroup={milgroup}') as response:
        data: list[dict[str, tp.Any]] = await response.json()

    for student in data:
        students.append(
            Student(
                id=student['id'],
                full_name=student['fullname']
            )
        )
    return students
 