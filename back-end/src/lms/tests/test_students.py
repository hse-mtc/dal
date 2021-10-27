import pytest


@pytest.fixture
def assert_student_equals():
    pass


@pytest.mark.django_db
def test_get_skills_by_student_id(create_student):
    create_student()
