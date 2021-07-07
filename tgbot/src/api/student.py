import typing as tp

from dataclasses import dataclass
from enum import (
    Enum,
    auto,
)

from api.client import client


class State(Enum):
    ABSENT = auto()
    PRESENT = auto()


@dataclass
class Milgroup:
    milgroup: str
    milfaculty: str
    weekday: int
    archived: bool


@dataclass
class Student:
    id: int
    fullname: str
    state: State
    milgroup: tp.Optional[Milgroup] = None
    absence_type: str = "NS"
    absence_status: str = "OP"
    post: str = "PL"  # TODO(vladisa88): add StudentPosts (Platoon Leader)

    def is_milgroup_commander(self) -> bool:
        # TODO(vladisa88): `PL` may change to something else in the future.
        return self.post == "PL"

    @staticmethod
    def from_raw(body: dict[str, tp.Any]) -> "Student":
        print(body)
        return Student(
            id=body["id"],
            fullname=body["fullname"],
            milgroup=Milgroup(**body["milgroup"]),
            state=State.PRESENT,
        )

    def to_body(self) -> dict[str, tp.Any]:
        return {
            "student": self.id,
            "absence_type": self.absence_type,
            "absence_status": self.absence_status,
        }


async def fetch_students(
    *args: tp.Any,
    many: bool = True,
    **kwargs: tp.Any,
) -> tp.Union[Student, list[Student]]:
    """Fetch students filtering by params."""

    response = await client.get("lms/students/", *args, **kwargs)
    data: list[dict[str, tp.Any]] = await response.json()
    students = [Student.from_raw(body) for body in data]

    if many:
        return students
    else:
        return students[0]


async def fetch_milgroup_leader_phones(
    milfaculty: str,
    *args: tp.Any,
    **kwargs: tp.Any,
) -> list[str]:
    method = "lms/milgroup-leaders/"
    params = {"milfaculty": milfaculty}
    response = await client.get(method, *args, params=params, **kwargs)
    data: dict[str, list[str]] = await response.json()
    return data["phones"]
