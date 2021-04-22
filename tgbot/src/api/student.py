import typing as tp

from dataclasses import dataclass
from enum import (
    Enum,
    auto,
)

from api.client import client

from utils.auth import auth_required


class State(Enum):
    absent = auto()
    present = auto()


@dataclass
class Student:
    id: int
    full_name: str
    state: State
    milgroup: str
    absence_type: str = 'NS'
    absence_status: str = 'OP'
    post: str = 'PL' # TODO: add StudentPosts (Platoon Leader)

@auth_required
async def fetch_students(milgroup: str = None, phone: str = None, *args, **kwargs) -> list[Student]:
    if milgroup:
        url = f'?milgroup={milgroup}'
    elif phone:
        url = f'?phone={phone}'
    students = []
    async with client.get(f'lms/students{url}', *args, **kwargs) as response:
        data: list[dict[str, tp.Any]] = await response.json()
    for student in data:
        students.append(
            Student(id=student['id'],
                    full_name=student['fullname'],
                    state=State.present,
                    milgroup=student['milgroup']['milgroup']))
    return students
