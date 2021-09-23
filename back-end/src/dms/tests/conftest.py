# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
from typing import List

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from dms.models.documents import File

from auth.models import User
from lms.models.students import Student

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
def publisher_data():

    def call_me(name: str = "publisher name") -> dict:
        return {"name": name}

    return call_me


@pytest.fixture
def author_data():

    def call_me(surname: str = "last",
                name: str = "first",
                patronymic: str = "patronymic") -> dict:
        return {"surname": surname, "name": name, "patronymic": patronymic}

    return call_me


@pytest.fixture
def file():

    def call_me(name: str = "filename",
                content: str = "file content") -> ContentFile:
        content = ContentFile(content, name=name)
        instance = File.objects.create(content=content, name=name)
        instance.save()
        return instance

    return call_me


@pytest.fixture(scope="function")
def category_data():

    def call_me(index: int = 0) -> dict:
        return {
            "title": f"category_{index}",
        }

    return call_me


@pytest.fixture
def user():
    instance = get_user_model().objects.create_user(
        email="user@mail.com",
        password="password",
    )
    instance.save()
    return instance


@pytest.fixture
def paper_data(file):

    def call_me(file_name: str = "filename",
                file_content: str = "file content",
                tags: List[str] = None,
                title: str = "paper title",
                annotation: str = "some annotation",
                upload_date: str = "2021-09-17",
                publication_date: str = "2021-09-17",
                is_binned: bool = False):
        if tags is None:
            tags = []
        # pylint: disable=too-many-locals

        return {
            "content": ContentFile(file_content, name=file_name),
            "tags": tags,
            "title": title,
            "annotation": annotation,
            "upload_date": upload_date,
            "publication_date": publication_date,
            "is_binned": is_binned
        }

    return call_me


@pytest.fixture
def student_data():

    def call_me(
        name: str = "first",
        surname: str = "second",
        patronymic: str = "patronymic",
    ) -> tuple:
        # pylint: disable=too-many-locals

        s = Student()
        s.name = name
        s.surname = surname
        s.patronymic = patronymic
        return s, {
            "fullname": s.full_name,
            "name": s.name,
            "surname": s.surname,
            "patronymic": s.patronymic,
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
