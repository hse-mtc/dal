# pylint: disable=redefined-outer-name

from operator import itemgetter

import pytest

from dms.models.papers import (
    Category,
    Paper,
)


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    response = su_client.get("/api/dms/categories")
    assert response.status_code == 301

    response = su_client.get("/api/dms/categories/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_categories_creates_new_category(su_client, category_data):
    first = su_client.post("/api/dms/categories/", category_data(1))
    assert first.status_code == 201

    second = su_client.post("/api/dms/categories/", category_data(2))
    assert second.status_code == 201

    assert first.data["id"] != second.data["id"]


@pytest.mark.django_db
def test_get_categories_returns_list(su_client, category_data):
    # pylint: disable=too-many-locals

    count = 3
    for i in range(count):
        Category.objects.create(**category_data(i))

    response = su_client.get("/api/dms/categories/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, category in enumerate(response.data, start=min_id):
        data = category_data(id_ - min_id)
        data["additional_schema"] = None
        data["id"] = id_
        assert category == data


@pytest.mark.django_db
def test_get_category_by_id_returns_single_category(su_client, category_data):
    data = category_data()
    id_ = Category.objects.create(**data).id
    data["id"] = id_
    data["additional_schema"] = None

    response = su_client.get(f"/api/dms/categories/{id_}/")
    assert response.status_code == 200
    assert response.data == data


@pytest.mark.django_db
def test_delete_category_removes_category_from_db(su_client, category_data):
    id_ = Category.objects.create(**category_data()).id

    response = su_client.delete(f"/api/dms/categories/{id_}/")
    assert response.status_code == 204

    assert not Category.objects.exists()


@pytest.mark.django_db
def test_delete_category_with_papers_fails(
    su_client,
    category_data,
    file,
    user,
):
    category = Category.objects.create(**category_data())
    paper = Paper.objects.create(
        file=file(),
        category=category,
        user=user,
    )

    response = su_client.delete(f"/api/dms/categories/{category.id}/")
    assert response.status_code == 422

    paper.delete()

    response = su_client.delete(f"/api/dms/categories/{category.id}/")
    assert response.status_code == 204


# TODO(TmLev): test Category.title uniqueness.
