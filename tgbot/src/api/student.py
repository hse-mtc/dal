import typing as tp

from dataclasses import dataclass
from enum import (
    Enum,
    auto,
)

from api.client import client


class State(Enum):
    LA = 0
    IL = 1
    LE = 2
    PRESENT = 3


class Post(Enum):
    GC = "командир взвода"
    SC = "командир отделения"


@dataclass
class Milfaculty:
    id: int
    title: str
    abbreviation: str


@dataclass
class Milgroup:
    id: int
    title: str
    milfaculty: Milfaculty
    weekday: int
    archived: bool
    milspecialty: int


@dataclass
class Student:
    id: int
    fullname: str
    state: State
    milgroup: tp.Optional[Milgroup] = None
    status: str = "OP"
    reason: str = ""
    post: tp.Optional[str] = None

    def is_milgroup_commander(self) -> bool:
        return self.post in ("GC", "SC")

    @staticmethod
    def from_raw(body: dict[str, tp.Any]) -> "Student":
        # remove unnecessary data
        for key in [
            "skills",
            "contact_info",
            "birth_info",
            "university_info",
            "family",
        ]:
            body.pop(key)

        # parse milgroup & milfaculty
        milgroup_dict = body.pop("milgroup")
        if milgroup_dict is None:
            milgroup = None
        else:
            milfaculty = Milfaculty(**milgroup_dict.pop("milfaculty"))
            milgroup = Milgroup(milfaculty=milfaculty, **milgroup_dict)

        return Student(
            id=body["id"],
            fullname=body["fullname"],
            milgroup=milgroup,
            state=State.PRESENT,
            post=body["post"],
        )

    def to_body(self) -> dict[str, tp.Any]:
        return {
            "student": self.id,
            "excuse": self.state.name,
            "status": self.status,
        }


async def fetch_students(
    *args: tp.Any,
    many: bool = True,
    authorizing: bool = False,
    **kwargs: tp.Any,
) -> tp.Union[list[Student], Student]:
    """Fetch students filtering by params."""

    response = await client.get("lms/students/", *args, **kwargs)
    data: list[dict[str, tp.Any]] = await response.json()
    students = [Student.from_raw(body) for body in data]

    # Return data as is if we are authorizing the user.
    if authorizing:
        return students

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
