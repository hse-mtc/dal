# pylint: disable=redefined-outer-name

from operator import itemgetter

import pytest

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

from dms.models.documents import File
from dms.models.papers import (
    Category,
    Paper,
)


@pytest.fixture(scope="function")
def category_data():
    return {
        "title": "category",
    }


@pytest.fixture(scope="function")
def file():
    name = "name"
    content = ContentFile("some content here", name=name)
    instance = File.objects.create(content=content, name=name)
    instance.save()
    return instance


@pytest.fixture(scope="function")
def user():
    instance = get_user_model().objects.create_user(
        email="user@mail.com",
        password="password",
    )
    instance.save()
    return instance


@pytest.mark.django_db
def test_trailing_slash_redirect(client):
    response = client.get("/api/dms/categories")
    assert response.status_code == 301

    response = client.get("/api/dms/categories/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_categories_creates_new_category(client, category_data):
    first = client.post("/api/dms/categories/", category_data)
    assert first.status_code == 201

    second = client.post("/api/dms/categories/", category_data)
    assert second.status_code == 201

    assert first.data["id"] != second.data["id"]


@pytest.mark.django_db
def test_get_categories_returns_list(client, category_data):
    # pylint: disable=too-many-locals

    count = 3
    for _ in range(count):
        Category.objects.create(**category_data)

    response = client.get("/api/dms/categories/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, category in enumerate(response.data, start=min_id):
        category_data["id"] = id_
        assert category == category_data


@pytest.mark.django_db
def test_get_category_by_id_returns_single_category(client, category_data):
    id_ = Category.objects.create(**category_data).id
    category_data["id"] = id_

    response = client.get(f"/api/dms/categories/{id_}/")
    assert response.status_code == 200
    assert response.data == category_data


@pytest.mark.django_db
def test_delete_category_removes_category_from_db(client, category_data):
    id_ = Category.objects.create(**category_data).id

    response = client.delete(f"/api/dms/categories/{id_}/")
    assert response.status_code == 204

    assert not Category.objects.exists()


@pytest.mark.django_db
def test_delete_category_with_papers_fails(client, category_data, file, user):
    category = Category.objects.create(**category_data)
    paper = Paper.objects.create(
        file=file,
        category=category,
        user=user,
    )

    response = client.delete(f"/api/dms/categories/{category.id}/")
    assert response.status_code == 422

    paper.delete()

    response = client.delete(f"/api/dms/categories/{category.id}/")
    assert response.status_code == 204
