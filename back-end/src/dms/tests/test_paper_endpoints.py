# pylint: disable=redefined-outer-name
import random

import pytest

from dms.models.papers import Category
from dms.models.documents import File
from dms.models.common import Author, Publisher


@pytest.fixture
def non_string_publication_data(author_data, publisher_data, category_data):

    def call_me(num_authors: int = 1, num_publishers: int = 1):

        return {
            "authors": [
                Author.objects.create(**author_data()).id
                for _ in range(num_authors)
            ],
            "publishers": [
                Publisher.objects.create(**publisher_data()).id
                for _ in range(num_publishers)
            ],
            "category": Category.objects.create(**category_data()).id
        }

    return call_me


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    response = su_client.get("/api/dms/papers")
    assert response.status_code == 301

    response = su_client.get("/api/dms/papers/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_papers_creates_new_paper(su_client, paper_data,
                                       non_string_publication_data):
    data = paper_data()
    data |= non_string_publication_data()
    response = su_client.post("/api/dms/papers/", data)
    assert response.status_code == 201
    id_ = response.data["id"]

    response = su_client.get(f"/api/dms/papers/{id_}/")
    assert response.status_code == 200

    file = File.objects.get(
        id=response.data["file"]["content"].rsplit("/", maxsplit=1)[-1])
    to_compare_fields = [
        "title", "annotation", "upload_date", "publication_date", "is_binned",
        "category", "authors", "publishers"
    ]
    assert file.content.open("r").read() == data["content"].open("r").read()
    assert {
        field_name: response.data[field_name]
        for field_name in to_compare_fields
    } == {field_name: data[field_name] for field_name in to_compare_fields}


@pytest.mark.django_db
def test_get_searches_papers_by_title_and_annotation(
        su_client, paper_data, non_string_publication_data):
    data = paper_data(title="Танки Великой Отечественной войны")
    non_string_data = non_string_publication_data()
    data |= non_string_data
    response = su_client.post("/api/dms/papers/", data)
    assert response.status_code == 201

    for _ in range(5):
        data = paper_data(
            title=random.choice(["Тактика боя", "Устав", "Справочник офицера"]))
        data |= non_string_data
        response = su_client.post("/api/dms/papers/", data)
        assert response.status_code == 201

    response = su_client.get("/api/dms/papers/", {"search": "танк"})
    assert response.status_code == 200
    assert len(response.data) == 1

    data = paper_data(title="Танки США и NATO")
    data |= non_string_data
    response = su_client.post("/api/dms/papers/", data)
    assert response.status_code == 201

    response = su_client.get("/api/dms/papers/", {"search": "танк"})
    assert response.status_code == 200
    assert len(response.data) == 2
