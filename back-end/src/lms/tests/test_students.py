import pytest


@pytest.fixture
def assert_student_equals():
    pass


@pytest.mark.django_db
def test_get_skills_by_student_id(su_client, create_student, get_student_data):
    student, student_ids = create_student()
    data = get_student_data(student_ids=student_ids)

    response = su_client.get(f'/api/lms/students/skills/{student.id}/')
    assert response.status_code == 200

    assert response.data['skills'] == data['skills']


@pytest.mark.django_db
def test_get_all_students(su_client, create_student):
    students_ids = []
    #pylint: disable=unused-variable
    for i in range(3):
        _, students_id = create_student()
        students_ids.append(students_id)

    response = su_client.get('/api/lms/students/')
    print(response)
