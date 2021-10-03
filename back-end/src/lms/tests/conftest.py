# pylint: disable=unused-argument,redefined-outer-name,import-outside-toplevel,invalid-name, too-many-locals, too-many-arguments
import base64
from io import BytesIO

import pytest
from django.core.files import File

from conf.settings import BASE_DIR

from common.models.persons import Photo
from PIL import Image

from auth.models import User
from lms.models.students import Student

SUPERUSER_EMAIL = "superuserfortests@mail.com"
SUPERUSER_PASSWORD = "superuserpasswordfortests"


@pytest.fixture
def superuser(db):
    user = User.objects.filter(email=SUPERUSER_EMAIL)
    if user.exists():
        return user.first()

    return User.objects.create_superuser(
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD,
    )


@pytest.fixture
def su_client(superuser):
    from django.test.client import Client
    response = Client().post(
        "/api/auth/tokens/obtain/",
        {
            "email": SUPERUSER_EMAIL,
            "password": SUPERUSER_PASSWORD
        },
        content_type="application/json",
    )
    access_token = response.data["access"]
    return Client(HTTP_AUTHORIZATION=f"Bearer {access_token}")


@pytest.fixture
def student_status():
    pass


@pytest.fixture
def student_post():
    pass


@pytest.fixture
def student_milgroup():
    pass


@pytest.fixture
def student_milspecialty():
    pass


@pytest.fixture
def student_skills():
    pass


@pytest.fixture
def student_passport():
    pass


@pytest.fixture
def student_family():
    pass


@pytest.fixture
def student_recruitment_office():
    pass


@pytest.fixture
def student_university_info():
    pass


@pytest.fixture
def student_application_process():
    pass


@pytest.fixture
@pytest.mark.django_db
def student_photo():

    def call_me() -> Photo:
        photo_ = Photo()
        img = Image.open(fp=BASE_DIR / 'src' / 'lms' / 'tests' /
                                  'data' / 'images' / 'test_photo.png')

        buffered = BytesIO()
        img.save(buffered, 'PNG')
        photo_.image.save('photo.png', File(buffered))
        return photo_

    return call_me


@pytest.fixture
@pytest.mark.django_db
def student_data(student_photo):

    def call_me(
        name: str = "first",
        surname: str = "second",
        patronymic: str = "patronymic",
    ) -> dict:

        s = Student()
        s.name = name
        s.surname = surname
        s.patronymic = patronymic
        s.photo = student_photo()
        s.save()

        photo_base64 = base64.b64encode(s.photo.image.read())

        return {
            "fullname": s.full_name,
            "name": s.name,
            "surname": s.surname,
            "patronymic": s.patronymic,
            "photo": photo_base64,
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
