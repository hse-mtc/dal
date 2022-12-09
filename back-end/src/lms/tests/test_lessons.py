# pylint: disable=redefined-outer-name

import pytest

from lms.models.lessons import Lesson


def unpack_lesson(lesson: Lesson, with_id: bool = False) -> dict:
    lesson_data = {
        "type": lesson.type,
        "date": lesson.date,
        "ordinal": lesson.ordinal,
        "subject": lesson.subject.id,
        "room": lesson.room.id,
        "milgroup": lesson.milgroup.id,
        "teacher": lesson.teacher.id,
    }
    if with_id:
        lesson_data["id"] = lesson.id

    return lesson_data


@pytest.mark.django_db
def test_trailing_slash_redirect(su_client):
    response_wrong = su_client.get("/api/lms/lessons")
    assert response_wrong.status_code == 301

    response_right = su_client.get("/api/lms/lessons/")
    assert response_right.status_code == 200


@pytest.mark.django_db
def test_post_posts_right_data(su_client, get_new_lesson_data):
    lesson_data = get_new_lesson_data()

    first_lesson_response = su_client.post(
        "/api/lms/lessons/", lesson_data, content_type="application/json"
    )

    second_lesson_response = su_client.post(
        "/api/lms/lessons/", lesson_data, content_type="application/json"
    )

    assert first_lesson_response.status_code == 201
    assert second_lesson_response.status_code == 201

    assert first_lesson_response.data.pop("id") != second_lesson_response.data.pop("id")

    assert first_lesson_response.data == lesson_data
    assert second_lesson_response.data == lesson_data


@pytest.mark.django_db
def test_get_by_id_returns_right_data(get_new_lesson_data, su_client, create_lesson):
    lesson_data = get_new_lesson_data(ids_only=False)
    lesson = create_lesson(**lesson_data)
    lesson_data = unpack_lesson(lesson, with_id=True)

    lesson_response_get = su_client.get(f"/api/lms/lessons/{lesson.id}/")

    assert lesson_response_get.status_code == 200

    lesson_response_get = lesson_response_get.json()

    lesson_response_get["milgroup"] = lesson_response_get["milgroup"]["id"]
    lesson_response_get["subject"] = lesson_response_get["subject"]["id"]
    lesson_response_get["room"] = lesson_response_get["room"]["id"]
    lesson_response_get["teacher"] = lesson_response_get["teacher"]["id"]

    assert lesson_response_get == lesson_data


@pytest.mark.django_db
def test_put_changes_data(get_new_lesson_data, su_client, create_lesson):
    lesson_data = get_new_lesson_data(ids_only=False)
    lesson = create_lesson(**lesson_data)

    lesson_data = unpack_lesson(lesson)

    if lesson_data["type"] != "SE":
        new_type = "SE"
    else:
        new_type = "GR"
    lesson_data["type"] = new_type
    lesson_data["ordinal"] += 1

    lesson_response_put = su_client.put(
        f"/api/lms/lessons/{lesson.id}/", lesson_data, content_type="application/json"
    )

    assert lesson_response_put.status_code == 200
    assert lesson_response_put.data["type"] == new_type
    assert lesson_response_put.data["type"] != lesson.type
    assert lesson_response_put.data["ordinal"] - 1 == lesson.ordinal


@pytest.mark.django_db
def test_patch_patches_data(
    get_new_lesson_data,
    su_client,
    create_lesson,
):
    lesson_data = get_new_lesson_data(ids_only=False)
    first_lesson_data = create_lesson(**lesson_data)

    if lesson_data["type"] != "SE":
        new_type = "SE"
    else:
        new_type = "GR"
    new_values = {"type": new_type, "ordinal": lesson_data["ordinal"] + 1}

    lesson_response_patch = su_client.patch(
        f"/api/lms/lessons/{first_lesson_data.id}/",
        new_values,
        content_type="application/json",
    )

    assert lesson_response_patch.status_code == 200
    assert lesson_response_patch.data["type"] == new_values["type"]
    assert lesson_response_patch.data["type"] != first_lesson_data.type
    assert lesson_response_patch.data["ordinal"] - 1 == first_lesson_data.ordinal


@pytest.mark.django_db
def test_delete_deletes_lesson(su_client, get_new_lesson_data, create_lesson):
    lesson_data = get_new_lesson_data(ids_only=False)
    first_lesson_data = create_lesson(**lesson_data)

    first_lesson_response = su_client.delete(
        f"/api/lms/lessons/{first_lesson_data.id}/", content_type="application/json"
    )

    assert first_lesson_response.status_code == 204
