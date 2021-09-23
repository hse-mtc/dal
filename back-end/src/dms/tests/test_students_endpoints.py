from operator import itemgetter

import pytest

from lms.models.students import Student


@pytest.fixture
def data_student():

    def call_me(
        name: str = "first",
        surname: str = "second",
        patronymic: str = "patronymic",
    ) -> tuple:

        s = Student()
        s.name = name
        s.surname = surname
        s.patronymic = patronymic
        return s, {
            "fullname": s.full_name,
            "name": s.name,
            "surname": s.surname,
            "patronymic": s.patronymic,
            "photo": s.photo,
            "milgroup": s.milgroup,
            "birth_info": s.birth_info,
            "university_info": s.university_info,
            "application_process": s.application_process,
            "skills": [],
            "contact_info": s.contact_info,
            "citizenship": s.citizenship,
            "permanent_address": s.permanent_address,
            "surname_genitive": s.surname_genitive,
            "name_genitive": s.name_genitive,
            "patronymic_genitive": s.patronymic_genitive,
            "status": s.status,
            "post": s.post,
            "user": s.user,
            "milspecialty": s.milspecialty,
            "passport": s.passport,
            "recruitment_office": s.recruitment_office,
            "family": []
        }

    return call_me


@pytest.mark.django_db
def test_get_students_returns_list(su_client, test_student):
    # pylint: disable=too-many-locals

    count = 3
    for _ in range(count):
        s, data = data_student()
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
