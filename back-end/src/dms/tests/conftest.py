# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
from typing import List
import datetime

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from auth.models import User
from lms.models.students import Student

from dms.models.common import Author, Publisher
from dms.models.documents import File

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
    # pylint: disable=too-many-arguments
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
            "data": {
                "tags": tags,
                "title": title,
                "annotation": annotation,
                "upload_date": upload_date,
                "publication_date": publication_date,
                "is_binned": is_binned
            }
        }

    return call_me


@pytest.fixture()
def image(tmp_path):

    def call_me(name: str = "image.png") -> SimpleUploadedFile:
        image = Image.new("RGB", size=(1, 1))
        sub_dir = tmp_path / "sub"
        sub_dir.mkdir(parents=True, exist_ok=True)
        path = sub_dir / name
        image.save(str(path))
        content = ""
        with open(path, "rb") as file:
            content = file.read()
        return SimpleUploadedFile(name=name,
                                  content=content,
                                  content_type="image/png")

    return call_me


@pytest.fixture
def cover_data(image):

    def call_me(name: str = "image.png"):
        return {"image": image(name)}

    return call_me


@pytest.fixture
def subject_data(user):

    def call_me(title: str = "title", annotation: str = "annotation"):
        return {"title": title, "annotation": annotation, "user": user}

    return call_me


@pytest.fixture()
@pytest.mark.django_db
def book_data(image):
    # pylint: disable=too-many-arguments
    def call_me(
        author_data,
        publisher_data,
        subject_data,
        file_name: str = "filename",
        file_content: str = "file content",
        image_name: str = "image.png",
        title: str = "title",
        annotation: str = "annotation",
        upload_date: str = str(datetime.date.today()),
        publication_year: int = 2021,
        page_count: int = 100,
    ):
        author = Author.objects.create(**author_data())
        publisher = Publisher.objects.create(**publisher_data())
        subject = Subject.objects.create(**subject_data())
        return {
            "content": ContentFile(file_content, name=file_name),
            "image": image(image_name),
            "data": {
                "title": title,
                "annotation": annotation,
                "upload_date": upload_date,
                "publication_year": publication_year,
                "page_count": page_count,
                "authors": [author.id],
                "publishers": [publisher.id],
                "subjects": [subject.id]
            }
        }

    return call_me
