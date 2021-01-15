import typing as tp

from collections import namedtuple
from dataclasses import dataclass

from aiohttp import ClientResponse

from api.client import client


@dataclass
class Student:
    id: int
    full_name: str
    state: int = 0

student_states = []

async def fetch_students(milgroup: str) -> list[Student]:
    students = []
    async with client.get(f'lms/student?milgroup={milgroup}') as response:
        data: list[dict[str, tp.Any]] = await response.json()

    for student in data:
        student_states.append(
            Student(
                id=student['id'],
                full_name=student['fullname'],
                state=0
            )
        )
    return student_states
    