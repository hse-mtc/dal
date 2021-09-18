# pylint: disable=redefined-outer-name

from io import BytesIO
import pytest

from dms.models.papers import Category
from dms.models.documents import File
from dms.models.common import Author, Publisher


@pytest.fixture(scope="function")
def paper_data():
    return {
        "content": BytesIO(b"Some text"),
        "tags": {"tag 1", "tag 2"},
        "title": "paper title",
        "annotation": "some annotation",
        "upload_date": "2021-09-17",
        "publication_date": "2021-09-17",
        "is_binned": False
    }


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    response = su_client.get("/api/dms/papers")
    assert response.status_code == 301

    response = su_client.get("/api/dms/papers/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_papers_creates_new_paper(su_client, author_data, publisher_data,
                                       category_data, paper_data):
    author_id_ = Author.objects.create(**author_data()).id
    publisher_id_ = Publisher.objects.create(**publisher_data()).id
    category_id_ = Category.objects.create(**category_data()).id

    paper_data |= {
        "authors": [author_id_],
        "publishers": [publisher_id_],
        "category": category_id_
    }
    response = su_client.post("/api/dms/papers/", paper_data)
    assert response.status_code == 201
    id_ = response.data["id"]

    response = su_client.get(f"/api/dms/papers/{id_}/")
    assert response.status_code == 200

    file = File.objects.get(
        id=response.data["file"]["content"].rsplit("/", maxsplit=1)[-1])
    assert file.content.open().read() == paper_data["content"].getvalue()
    to_compare_fields = [
        "title", "annotation", "upload_date", "publication_date", "is_binned",
        "category", "authors", "publishers"
    ]
    assert {
        field_name: response.data[field_name]
        for field_name in to_compare_fields
    } == {
        field_name: paper_data[field_name] for field_name in to_compare_fields
    }
