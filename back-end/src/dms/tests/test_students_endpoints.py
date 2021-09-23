from operator import itemgetter

import pytest

from dms.models.common import Author
from lms.models.students import Student

@pytest.fixture
def student_data():

    def call_me(surname: str = "stud_last",
                name: str = "stud_first",
                patronymic: str = "stud_patronymic") -> dict:
        return {"surname": surname, "name": name, "patronymic": patronymic}

    return call_me

@pytest.mark.django_db
def test_get_students_returns_list(su_client, student_data):
    # pylint: disable=too-many-locals

    count = 3
    data = student_data()
    for _ in range(count):
        Author.objects.create(**data)
        Student.objects.create(**data)
    print(Author.objects.get(id=1))

    response = su_client.get("/api/lms/students/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, student in enumerate(response.data, start=min_id):
        data["id"] = id_
        assert student == data