# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
from typing import List

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from dms.models.documents import File

from auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile

from dms.models.books import Cover
from dms.models.common import Author, Publisher
from common.models.subjects import Subject

from PIL import Image

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


@pytest.fixture()
def image(tmp_path):
    def call_me(name: str = "image.png") -> SimpleUploadedFile:
        image =  Image.new('RGB', size=(1, 1))
        dir = tmp_path / "sub"
        dir.mkdir(parents=True, exist_ok=True)
        path = dir / name
        image.save(str(path))
        return SimpleUploadedFile(name=name, content=open(path, 'rb').read(), content_type='image/png')

    return call_me


@pytest.fixture
def cover_data(image):
    def call_me(name: str = "image.png"):
        return {
            'image': image(name)
        }
    
    return call_me


@pytest.fixture
def subject_data(user):
    def call_me(title: str = "title",
                annotation: str = "annotation") -> SimpleUploadedFile:
        return {
            'title': title,
            'annotation': annotation,
            'user': user
        }

    return call_me


@pytest.fixture()
@pytest.mark.django_db
def book_data(image):
    # pylint: disable=too-many-arguments
    def call_me(cover_data,
                author_data,
                publisher_data,
                subject_data,
                file_name: str = "filename",
                file_content: str = "file content", 
                image_name: str = "image.png"):
        cover = Cover.objects.create(**cover_data())
        author = Author.objects.create(**author_data())
        publisher = Publisher.objects.create(**publisher_data())
        subject = Subject.objects.create(**subject_data())
        return {
            "content": ContentFile(file_content, name=file_name),
            "image": image(image_name),
            "title": "string",
            "annotation": "string",
            "upload_date": "2021-09-23",
            "publication_year": 32767,
            "page_count": 32767,
            "cover": cover.id,
            "authors": [
                author.id
            ],
            "publishers": [
                publisher.id
            ],
            "subjects": [
                subject.id
            ]
        }

    return call_me