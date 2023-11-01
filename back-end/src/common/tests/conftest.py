import pytest

from auth.models import User
from common.models.milspecialties import Milspecialty
from common.models.subjects import Subject


@pytest.fixture
def create_milspeciality():
    def call_me(title: str, code: str, available_for=None):
        if available_for is None:
            available_for = ["MO"]
        milspeciality, _ = Milspecialty.objects.get_or_create(
            title=title,
            code=code,
            available_for=available_for,
        )
        return milspeciality

    return call_me


@pytest.fixture
def create_subject():
    def call_me(
        user: User,
        milspecialty: Milspecialty,
        title: str = "Тактическая подготовка 2",
        annotation: str = None,
    ):
        if annotation is None:
            annotation = f"Пример анноттации для {title}"
        subject, _ = Subject.objects.get_or_create(
            milspecialty=milspecialty,
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
        milspecialty: int,
        title: str = "Тактическая подготовка 2",
        annotation: str = None,
    ):
        if annotation is None:
            annotation = f"Пример анноттации для {title}"
        user = create_test_user()
        data = {
            "milspecialty": milspecialty,
            "title": title,
            "annotation": annotation,
            "user": user,
        }
        return data

    return call_me
