import typing as tp

from dataclasses import dataclass
from enum import (
    Enum,
    auto,
)

from api.client import client

from utils.auth import check_token


class State(Enum):
    absent = auto()
    present = auto()


@dataclass
class Student:
    id: int
    full_name: str
    state: State
    absence_type: str = 'Неуважительная'
    absence_status: str = 'Открыт'


@check_token
async def fetch_students(milgroup: str, *args, **kwargs) -> list[Student]:
    students = []
    async with client.get(f'lms/students?milgroup={milgroup}', *args, **kwargs) as response:
        data: list[dict[str, tp.Any]] = await response.json()
    for student in data:
        students.append(
            Student(id=student['id'],
                    full_name=student['fullname'],
                    state=State.present))
    return students
