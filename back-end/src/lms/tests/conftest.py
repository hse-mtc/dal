# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name,too-many-arguments,redefined-builtin

from typing import List
from datetime import datetime

import pytest

from django.contrib.auth import get_user_model

from common.models.subjects import Subject

from lms.models.teachers import Teacher
from lms.models.lessons import (
    Room,
    Lesson,
)
from lms.models.common import (
    Milfaculty,
    Milgroup,
)


SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


User = get_user_model()


@pytest.fixture
def superuser(db):
    user = User.objects.filter(email=SUPERUSER_EMAIL)
    if user.exists():
        return user.first()

    return User.objects.create_superuser(
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )


@pytest.fixture
def su_client(superuser):
    from django.test.client import Client

    response = Client().post(
        "/api/auth/tokens/obtain/",
        {
            "email": SUPERUSER_EMAIL,
            "password": SUPERUSER_PASSWORD
        },
        content_type="application/json",
    )
    access_token = response.data["access"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {access_token}")


@pytest.fixture
def get_new_lesson_data() -> dict:

    def call_me(ids_only: bool = True):
        user = create_test_user()

        subject = create_subject(user)

        room = create_room()

        milfaculty = create_milfaculty()

        milgroup = create_milgroup(milfaculty=milfaculty)

        teacher = create_teacher(
            rank=Teacher.Rank.LIEUTENANT_COLONEL.value,
            milfaculty=milfaculty,
        )

        if ids_only:
            res = {
                "subject": subject.id,
                "room": room.id,
                "milgroup": milgroup.id,
                "teacher": teacher.id,
                "type": "LE",
                "date": "2021-09-22",
                "ordinal": 2,
            }
        else:
            res = {
                "subject": subject,
                "room": room,
                "milgroup": milgroup,
                "teacher": teacher,
                "type": "LE",
                "date": "2021-09-22",
                "ordinal": 2,
            }

        return res

    return call_me


def create_room(title: str = "510") -> Room:
    room, _ = Room.objects.get_or_create(title=title,)

    return room


def create_milfaculty(title: str = "Тестовое название цикла 1",
                      abbreviation: str = "АБР 1") -> Milfaculty:
    milfaculty, _ = Milfaculty.objects.get_or_create(title=title,
                                                     abbreviation=abbreviation)
    return milfaculty


def create_milgroup(
    milfaculty: Milfaculty,
    title: str = "Тестовое название взвода 1",
    weekday: int = 1,
) -> Milgroup:
    milgroup, _ = Milgroup.objects.get_or_create(title=title,
                                                 milfaculty=milfaculty,
                                                 weekday=weekday)

    return milgroup


def create_teacher(rank: str,
                   milfaculty: Milfaculty,
                   milgroups: List[Milgroup] or None = None) -> Teacher:
    value = {
        "surname": "Тест_Фам",
        "name": "Тест_Им",
        "patronymic": "Тест_От",
        "rank": rank,
        "post": Teacher.Post.MILFACULTY_HEAD.value,
        "milfaculty": milfaculty,
    }
    teacher, _ = Teacher.objects.get_or_create(**value)
    if milgroups:
        teacher.milgroups.add(*milgroups)

    return teacher


def create_subject(user: User,
                   title: str = "Тактическая подготовка 2") -> Subject:
    subject, _ = Subject.objects.get_or_create(
        title=title,
        annotation=f"Пример аннотации для '{title.lower()}'",
        user=user,
    )

    return subject


@pytest.fixture
def create_lesson():

    def call_me(
        room: Room,
        milgroup: Milgroup,
        subject: Subject,
        teacher: Teacher,
        type: str = "SE",
        date: datetime = "2021-09-22",
        ordinal: int = 1,
    ) -> Lesson:
        lesson, _ = Lesson.objects.get_or_create(
            room=room,
            subject=subject,
            milgroup=milgroup,
            type=type,
            date=date,
            ordinal=ordinal,
            teacher=teacher,
        )
        return lesson

    return call_me


def create_test_user(email: str = "test@email.ru", password: str = "1234"):
    user = User.objects.create_user(
        email=email,
        password=password,
        is_staff=True,
        is_superuser=False,
    )

    return user
