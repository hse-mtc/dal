# pylint: disable=redefined-outer-name

import pytest

from lms.models.lessons import Lesson


# TODO: надо вынести url отдельно, чтобы его не дублировать


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
    response_wrong = su_client.get("/api/lms/marks")
    assert response_wrong.status_code == 301

    response_right = su_client.get("/api/lms/marks/")
    assert response_right.status_code == 200


# @pytest.mark.django_db
# def test_post_posts_right_data(su_client, get_new_lesson_data):
#     lesson_data = get_new_lesson_data()

#     first_lesson_response = su_client.post("/api/lms/marks/",
#                                            lesson_data,
#                                            content_type="application/json")

#     second_lesson_response = su_client.post("/api/lms/marks/",
#                                             lesson_data,
#                                             content_type="application/json")

#     assert first_lesson_response.status_code == 201
#     assert second_lesson_response.status_code == 201

#     assert first_lesson_response.data.pop(
#         "id") != second_lesson_response.data.pop("id")

#     assert first_lesson_response.data == lesson_data
#     assert second_lesson_response.data == lesson_data