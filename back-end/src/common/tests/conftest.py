# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name,too-many-arguments,redefined-builtin
import pytest

from auth.models import User
from common.models.subjects import Subject

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


@pytest.fixture
def create_subject():
    def call_me(
            user: User,
            title: str = "Тактическая подготовка 2",
            annotation: str = None,
    ):
        if annotation is None:
            annotation = f'Пример анноттации для {title}'
        subject, _ = Subject.objects.get_or_create(
            title=title,
            annotation=annotation,
            user=user,
        )
        return subject

    return call_me


def create_test_user(email: str = "test@email.ru", password: str = "1234"):
    user = User.objects.create_user(
        email=email,
        password=password,
        is_staff=True,
        is_superuser=False,
    )

    return user


@pytest.fixture
def get_new_subject_data():

    def call_me(
            title: str = "Тактическая подготовка 2",
            annotation: str = None,
    ):
        if annotation is None:
            annotation = f'Пример анноттации для {title}'
        user = create_test_user()
        data = {
            "title": title,
            "annotation": annotation,
            "user": user,
        }
        return data

    return call_me
