import pytest


@pytest.fixture
def assert_student_equals():
    pass


@pytest.mark.django_db
def test_get_skills_by_student_id(su_client, create_student, get_student_data):
    stud = create_student
    data = get_student_data(stud_id=stud.id)

    response = su_client.get(f"/api/lms/students/skills/{stud.id}/")
    assert response.status_code == 200

    assert response.data["skills"] == data["skills"]
