from io import BytesIO
from operator import itemgetter

import pytest
import requests
from PIL.Image import Image


@pytest.mark.django_db
def test_get_students_returns_list(su_client, student_data):
    # pylint: disable=too-many-locals

    count = 3
    for _ in range(count):
        data = student_data()

    response = su_client.get("/api/lms/students/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, student in enumerate(response.data, start=min_id):
        data["id"] = id_
        # Server return an url to photo, not a base64 string!
        response = su_client.get(student["photo"]["image"])
        img = BytesIO(response.content)
        assert data["photo"] == img

        data["photo"] = student["photo"]
        assert student == data
