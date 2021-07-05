# pylint: disable=redefined-outer-name

from operator import itemgetter

import pytest

from dms.models.common import Author


@pytest.fixture(scope="function")
def author_data():
    return {
        "surname": "last",
        "name": "first",
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

    count = 3
    for _ in range(count):
        Author.objects.create(**author_data)

    response = client.get("/api/dms/authors/")
    assert response.status_code == 200
    assert len(response.data) == count

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


@pytest.mark.django_db
def test_patch_author_accepts_some_fields(client, author_data):
    id_ = Author.objects.create(**author_data).id

    data = {"surname": "second"}
    response = client.patch(
        f"/api/dms/authors/{id_}/",
        data,
        content_type="application/json",
    )
    assert response.status_code == 200

    author = Author.objects.get(id=id_)
    assert response.data["surname"] == author.surname


@pytest.mark.django_db
def test_put_author_requires_all_fields(client, author_data):
    id_ = Author.objects.create(**author_data).id

    data = {"surname": "second"}
    response = client.put(
        f"/api/dms/authors/{id_}/",
        data,
        content_type="application/json",
    )
    assert response.status_code == 400

    data = dict(author_data)
    data["surname"] = "second"
    response = client.put(
        f"/api/dms/authors/{id_}/",
        data,
        content_type="application/json",
    )
    assert response.status_code == 200

    response.data.pop("id")
    assert response.data == data


@pytest.mark.django_db
def test_delete_author_removes_author_from_db(client, author_data):
    id_ = Author.objects.create(**author_data).id

    response = client.delete(f"/api/dms/authors/{id_}/")
    assert response.status_code == 204

    assert not Author.objects.exists()
