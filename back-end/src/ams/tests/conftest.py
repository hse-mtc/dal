# pylint: disable=redefined-outer-name,invalid-name
from datetime import date

import pytest

from auth.models import User
from common.models.personal import BirthInfo, ContactInfo, Passport
from common.models.universities import Faculty, Program, UniversityInfo
from common.models.milspecialties import Milspecialty

from ams.models.applicants import Applicant, ApplicationProcess


@pytest.fixture
def application_process(db):
    """Пустой ApplicationProcess (все поля с дефолтами)."""
    return ApplicationProcess.objects.create()


@pytest.fixture
def applicant(db):
    """Минимальный абитуриент со всеми обязательными связями."""
    user = User.objects.create_user(
        email="override_applicant@edu.hse.ru", password="qwerty"
    )
    birth = BirthInfo.objects.create(
        date=date(2007, 3, 7), country="Россия", place="Москва"
    )
    passport = Passport.objects.create(
        series="1000",
        code="222222",
        ufms_name="УФМС",
        ufms_code="740-056",
        issue_date=date(2020, 10, 2),
    )
    contact = ContactInfo.objects.create(
        corporate_email="override@edu.hse.ru",
        personal_email="override@ovr.ru",
        personal_phone_number="79990000000",
    )
    faculty = Faculty.objects.create(campus="MO", title="ФКН", abbreviation="ФКН")
    program = Program.objects.create(code="09.03.01", title="ИВТ", faculty=faculty)
    uni = UniversityInfo.objects.create(
        program=program, group="ГР", card_id="CARD", graduation_year=2024
    )
    milspec = Milspecialty.objects.create(
        title="ВУС", code="453100", available_for=["MO"]
    )
    ap = ApplicationProcess.objects.create()
    return Applicant.objects.create(
        surname="Тестов",
        name="Тест",
        patronymic="Тестович",
        surname_genitive="Тестова",
        name_genitive="Теста",
        patronymic_genitive="Тестовича",
        recruitment_office="Военкомат",
        birth_info=birth,
        passport=passport,
        university_info=uni,
        contact_info=contact,
        application_process=ap,
        milspecialty=milspec,
        user=user,
    )
