# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from dms.models.documents import File

from auth.models import User


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
