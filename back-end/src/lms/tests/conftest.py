# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name,too-many-arguments,redefined-builtin
from typing import List
from datetime import datetime

import base64
from io import BytesIO, StringIO
from PIL import Image

import pytest

from conf.settings import BASE_DIR

from auth.models import User
from common.models.persons import Photo
from lms.models.students import Student
from lms.models.lessons import Room, Lesson
from lms.models.common import Milfaculty, Milgroup
from lms.models.teachers import Teacher, Rank
from common.models.subjects import Subject

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


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

        rank = create_rank()

        teacher = create_teacher(rank=rank,
                                 milgroups=None,
                                 milfaculty=milfaculty)

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


def create_teacher(rank: Rank,
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


def create_rank(title: str = "Тестовый ранк 1") -> Rank:
    rank, _ = Rank.objects.get_or_create(title=title)
    return rank


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

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


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
def student_status():
    pass


@pytest.fixture
def student_post():
    pass


@pytest.fixture
def student_milgroup():
    pass


@pytest.fixture
def student_milspecialty():
    pass


@pytest.fixture
def student_skills():
    pass


@pytest.fixture
def student_passport():
    pass


@pytest.fixture
def student_family():
    pass


@pytest.fixture
def student_recruitment_office():
    pass


@pytest.fixture
def student_university_info():
    pass


@pytest.fixture
def student_application_process():
    pass


@pytest.fixture
def student_photo():

    def call_me() -> Photo:
        photo_ = Photo()
        photo_.image = Image.open(fp=BASE_DIR / 'src' / 'lms' / 'tests' /
                                  'data' / 'images' / 'test_photo.png')
        return photo_

    return call_me

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


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
def student_status():
    pass


@pytest.fixture
def student_post():
    pass

@pytest.fixture
def student_milgroup():
    pass

@pytest.fixture
def student_milspecialty():
    pass

@pytest.fixture
def student_skills():
    pass

@pytest.fixture
def student_passport():
    pass

@pytest.fixture
def student_family():
    pass

@pytest.fixture
def student_recruitment_office():
    pass

@pytest.fixture
def student_university_info():
    pass

@pytest.fixture
def student_application_process():
    pass


@pytest.fixture
def student_photo():
    pass


@pytest.fixture
def student_data():

    def call_me(
        name: str = "first",
        surname: str = "second",
        patronymic: str = "patronymic",
    ) -> tuple:

        s = Student()
        s.name = name
        s.surname = surname
        s.patronymic = patronymic

        buffered = BytesIO()
        student_photo().image.save(buffered, format="PNG")
        photo_base64 = base64.b64encode(buffered.getvalue())

        return s, {
            "fullname": s.full_name,
            "name": s.name,
            "surname": s.surname,
            "patronymic": s.patronymic,
            "photo": photo_base64,
            "photo": s.photo,
            "milgroup": s.milgroup,
            "birth_info": s.birth_info,
            "university_info": s.university_info,
            "application_process": s.application_process,
            "skills": [],
            "contact_info": s.contact_info,
            "citizenship": s.citizenship,
            "permanent_address": s.permanent_address,
            "surname_genitive": s.surname_genitive,
            "name_genitive": s.name_genitive,
            "patronymic_genitive": s.patronymic_genitive,
            "status": s.status,
            "post": s.post,
            "user": s.user,
            "milspecialty": s.milspecialty,
            "passport": s.passport,
            "recruitment_office": s.recruitment_office,
            "family": []
        }

    return call_me
