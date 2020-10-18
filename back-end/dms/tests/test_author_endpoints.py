# pylint: disable=redefined-outer-name

from operator import itemgetter

import pytest

from dms.models import Author


@pytest.fixture(scope="function")
def author_data():
    return {
        "last_name": "last",
        "first_name": "first",
        "patronymic": "patronymic",
    }


@pytest.mark.django_db
def test_trailing_slash_redirect(client):
    response = client.get("/api/dms/authors")
    assert response.status_code == 301

    response = client.get("/api/dms/authors/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_authors_creates_new_author(client, author_data):
    first = client.post("/api/dms/authors/", author_data)
    assert first.status_code == 201

    second = client.post("/api/dms/authors/", author_data)
    assert second.status_code == 201

    assert first.data["id"] != second.data["id"]


@pytest.mark.django_db
def test_get_authors_returns_list(client, author_data):
    # pylint: disable=too-many-locals

    for _ in range(3):
        Author.objects.create(**author_data)

    response = client.get("/api/dms/authors/")
    assert response.status_code == 200

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, author in enumerate(response.data, start=min_id):
        author_data["id"] = id_
        assert author == author_data


@pytest.mark.django_db
def test_get_author_by_id_returns_single_author(client, author_data):
    id_ = Author.objects.create(**author_data).id
    author_data["id"] = id_

    response = client.get(f"/api/dms/authors/{id_}/")
    assert response.status_code == 200
    assert response.data == author_data
