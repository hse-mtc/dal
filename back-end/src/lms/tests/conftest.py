# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name,too-many-arguments,redefined-builtin
from typing import List
from datetime import datetime
import pytest

from auth.models import User
from common.models.subjects import Subject
from common.models.persons import BirthInfo, ContactInfo, Relative
from lms.models.applicants import Passport
from lms.models.lessons import Room, Lesson
from lms.models.common import Milfaculty, Milgroup
from lms.models.teachers import Teacher, Rank


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


def create_test_birth_info(date: datetime = datetime.today(),
                           country: str = "Wonderland",
                           city: str = "Sin city") -> BirthInfo:
    __bt_info, _ = BirthInfo.objects.get_or_create(date=date,
                                                   country=country,
                                                   city=city)

    return __bt_info


def create_test_contact_info(
        corporate_email="Fool@corp.com",
        personal_email="Fool@mail.com",
        personal_phone_number="88005553535") -> ContactInfo:
    __ct_info, _ = ContactInfo.objects.get_or_create(
        corporate_email=corporate_email,
        personal_email=personal_email,
        personal_phone_number=personal_phone_number)

    return __ct_info


def get_test_person_data(name: str = "Test name",
                         surname: str = "Test surname",
                         patronymic: str = "Test patr",
                         citizenship: str = "Wonderland") -> dict:
    return {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "citizenship": citizenship,
        "birth_info": create_test_birth_info(),
        "contact_info": create_test_contact_info()
    }


def create_test_relative(type=Relative.Type.FATHER.value) -> Relative:
    value = get_test_person_data()
    value["type"] = type
    __relative, _ = Relative.objects.get_or_create(**value)

    return __relative


def create_passport(
    series: str = "4040",
    code: str = "404040",
    ufms_name: str = "Test ufms",
    ufms_code: str = "4040404",
    issue_date: datetime = datetime.today()
) -> Passport:
    value = {
        "series": series,
        "code": code,
        "ufms_name": ufms_name,
        "ufms_code": ufms_code,
        "issue_date": issue_date
    }

    __passport, _ = Passport.objects.get_or_create(**value)
    return __passport


def get_passport_data(
    series: str = "4040",
    code: str = "404040",
    ufms_name: str = "Test ufms",
    ufms_code: str = "4040404",
    issue_date: datetime = datetime.today()) -> dict:
    return {
        "series": series,
        "code": code,
        "ufms_name": ufms_name,
        "ufms_code": ufms_code,
        "issue_date": issue_date
    }


def get_student_data(
    name: str = 'first',
    surname: str = 'second',
    patronymic: str = 'patronymic',
) -> dict:

    __pass = ""

    return {
        "name": name,
        "surname": surname,
        "patronymic": patronymic,
        "fullname": " ".join([surname, name, patronymic]),
        "photo": __pass,
        "birth_info": __pass,
        "contact_info": __pass,
        "citizenship": __pass,
        "permanent_address": __pass,
        "surname_genitive": __pass,
        "name_genitive": __pass,
        "patronymic_genitive": __pass,
        "user": __pass,
        "status": __pass,
        "post": __pass,
        "milgroup": __pass,
        "milspecialty": __pass,
        "skills": __pass,
        "passport": get_passport_data(),
        "family": __pass,
        "recruitment_office": __pass,
        "university_info": __pass,
        "application_process": __pass
    }
