# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
from typing import List
import datetime

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from dms.models.class_materials import Topic, ClassMaterial, Section
from dms.models.common import Author, Publisher
from dms.models.documents import File

from common.models.subjects import Subject


@pytest.fixture
def publisher_data():
    def call_me(name: str = "publisher name") -> dict:
        return {"name": name}

    return call_me


@pytest.fixture
def author_data():
    def call_me(
        surname: str = "last", name: str = "first", patronymic: str = "patronymic"
    ) -> dict:
        return {"surname": surname, "name": name, "patronymic": patronymic}

    return call_me


@pytest.fixture
def file():
    def call_me(name: str = "filename", content: str = "file content") -> ContentFile:
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
    def call_me(
        file_name: str = "filename",
        file_content: str = "file content",
        tags: List[str] = None,
        title: str = "paper title",
        annotation: str = "some annotation",
        upload_date: str = "2021-09-17",
        publication_date: str = "2021-09-17",
        is_binned: bool = False,
    ):
        if tags is None:
            tags = []

        return {
            "content": ContentFile(file_content, name=file_name),
            "data": {
                "tags": tags,
                "title": title,
                "annotation": annotation,
                "upload_date": upload_date,
                "publication_date": publication_date,
                "is_binned": is_binned,
            },
        }

    return call_me


@pytest.fixture()
def image(tmp_path):
    def call_me(name: str = "image.png", size=1, color=(0, 0, 0)) -> SimpleUploadedFile:
        image = Image.new("RGB", size=(size, size))
        for i in range(size):
            for j in range(size):
                image.putpixel((i, j), color)
        sub_dir = tmp_path / "sub"
        sub_dir.mkdir(parents=True, exist_ok=True)
        path = sub_dir / name
        image.save(str(path))
        content = ""
        with open(path, "rb") as file:
            content = file.read()
        return SimpleUploadedFile(name=name, content=content, content_type="image/png")

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
                "subjects": [subject.id],
            },
        }

    return call_me


@pytest.fixture()
def create_subject(user):
    subj, _ = Subject.objects.get_or_create(
        title="title",
        annotation="annotation",
        user=user
    )
    return subj


@pytest.fixture()
def create_sections(create_subject):
    s, _ = Section.objects.get_or_create(
        title="title",
        subject=create_subject
    )
    return s


@pytest.fixture()
def create_topic(create_sections):
    t, _ = Topic.objects.get_or_create(
        title="title",
        annotation="annotations",
        section=create_sections
    )
    return t


@pytest.fixture()
def get_file_model_data():

    def call_me(raw_file_body: str = "new_file",
                file_name: str = "file.txt") -> dict:
        values = {
            "name": file_name,
            "content": ContentFile(raw_file_body, name=file_name),
            "extension": file_name.rsplit(".", maxsplit=1)[-1]
        }
        return values

    return call_me


@pytest.fixture()
def create_file_model(get_file_model_data):

    def call_me(values=get_file_model_data()):
        val_cp = values.copy()
        val_cp.pop("extension")
        f, _ = File.objects.get_or_create(val_cp)
        return f

    return call_me


@pytest.fixture()
# pylint-disable: too-many-arguments
def get_class_material_data(user, get_file_model_data):

    def call_me(
        topic_id,
        title="title",
        annotation="annotation",
        type_=ClassMaterial.Type.LECTURES.value,
        upload_date: str = str(datetime.date.today())
    ) -> dict:
        values = {
            "file": get_file_model_data(),
            "title": title,
            "annotation": annotation,
            "upload_date": upload_date,
            "type": type_,
            "topic": topic_id
        }
        return values

    return call_me


@pytest.fixture()
def create_class_materials(get_class_material_data, create_file_model,
                           create_topic, user):

    def call_me():
        data = get_class_material_data(0)
        cm = ClassMaterial(
            type="LE",
            topic=create_topic,
            file=create_file_model(),
            title=data["title"],
            annotation=data["annotation"],
            user=user
        )
        cm.save()
        return cm

    return call_me
