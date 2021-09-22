import pytest
from lms.models.students import Student

@pytest.fixture
def student_data():

    def call_me(surname: str = "last",
                name: str = "first",
                patronymic: str = "patronymic") -> dict:
        return {"surname": surname, "name": name, "patronymic": patronymic}

    return call_me

@pytest.mark.django_db
def test_get_students_returns_list(su_client, author_data):
    # pylint: disable=too-many-locals

    count = 3
    data = author_data()
    for _ in range(count):
        Student.objects.create(**data)

    response = su_client.get("/api/lms/authors/")
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter("id")
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)["id"]

    for id_, author in enumerate(response.data, start=min_id):
        data["id"] = id_
        assert author == data