from operator import itemgetter

import pytest

@pytest.mark.django_db
def test_get_students_returns_list(su_client, student_data):
    # pylint: disable=too-many-locals

    count = 3
    for _ in range(count):
        s, data = student_data()
        s.save()

    response = su_client.get("/api/lms/students/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, student in enumerate(response.data, start=min_id):
        data["id"] = id_
        assert student == data
