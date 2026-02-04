# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name
import datetime
from typing import List

import pytest
from common.models.milspecialties import Milspecialty
from common.models.subjects import Subject
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from dms.models.class_materials import Section, Topic
from dms.models.common import Author, Publisher
from dms.models.documents import File
from dms.models.papers import Category
from PIL import Image


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
    import uuid

    def call_me(index: int = None) -> dict:
        if index is None:
            # Generate unique name using UUID
            unique_suffix = str(uuid.uuid4())[:8]
            return {"title": f"category_{unique_suffix}"}
        return {"title": f"category_{index}"}

    return call_me


@pytest.fixture
def non_string_paper_data(author_data, publisher_data, category_data):
    def call_me(num_authors: int = 1, num_publishers: int = 1):
        return {
            "authors": [
                Author.objects.create(**author_data()).id for _ in range(num_authors)
            ],
            "publishers": [
                Publisher.objects.create(**publisher_data()).id
                for _ in range(num_publishers)
            ],
            "category": Category.objects.create(**category_data()).id,
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


# ------
# Subject 1:
#   Section 1:
#     Topic 1
#     Topic 2
#     Topic 3
#   Section 2:
#     Topic 4
#     Topic 5
#   Section 3:
#   Section 4:
#     Topic 6
#     Topic 7
# Subject 2:
#   Section 5:
#     Topic 8
#   Section 6:
#     Topic 9


@pytest.fixture
def milspec():
    return Milspecialty.objects.create(
        title="Test milspec", code="123456", available_for=["MO"]
    )


@pytest.fixture
def subject1(milspec):
    return Subject.objects.create(
        title="Subject S1", annotation="Annotation for subject 1", milspecialty=milspec
    )


@pytest.fixture
def subject2(milspec):
    return Subject.objects.create(
        title="Subject S2", annotation="Annotation for subject 2", milspecialty=milspec
    )


@pytest.fixture
def section1(subject1):
    return Section.objects.create(title="Section 1", subject=subject1)


@pytest.fixture
def section2(subject1):
    return Section.objects.create(title="Section 2", subject=subject1)


@pytest.fixture
def section3(subject1):
    return Section.objects.create(title="Section 3", subject=subject1)


@pytest.fixture
def section4(subject1):
    return Section.objects.create(title="Section 4", subject=subject1)


@pytest.fixture
def section5(subject2):
    return Section.objects.create(title="Section 5", subject=subject2)


@pytest.fixture
def section6(subject2):
    return Section.objects.create(title="Section 5", subject=subject2)


@pytest.fixture
def topic1(section1):
    return Topic.objects.create(title="Topic 1", section=section1)


@pytest.fixture
def topic2(section1):
    return Topic.objects.create(title="Topic 2", section=section1)


@pytest.fixture
def topic3(section1):
    return Topic.objects.create(title="Topic 3", section=section1)


@pytest.fixture
def topic4(section2):
    return Topic.objects.create(title="Topic 4", section=section2)


@pytest.fixture
def topic5(section2):
    return Topic.objects.create(title="Topic 5", section=section2)


@pytest.fixture
def topic6(section4):
    return Topic.objects.create(title="Topic 6", section=section4)


@pytest.fixture
def topic7(section4):
    return Topic.objects.create(title="Topic 7", section=section4)


@pytest.fixture
def topic8(section5):
    return Topic.objects.create(title="Topic 8", section=section5)


@pytest.fixture
def topic9(section6):
    return Topic.objects.create(title="Topic 9", section=section6)
