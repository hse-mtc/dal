"""Questionnaire validation without a database or external services."""

import base64
from copy import deepcopy
from datetime import date
from io import BytesIO
from unittest.mock import Mock

import pytest
from PIL import Image

from auth.models import User
from ams.serializers.applicants import ApplicantMutateSerializer
from ams.serializers.validation import MAX_PHOTO_SIZE_BYTES
from common.models.milspecialties import Milspecialty
from common.models.universities import Faculty, Program


@pytest.fixture(autouse=True)
def remove_permissions():
    # Override the global fixture: these tests exercise validation, not the DB.
    yield


def image_data(format_="PNG"):
    output = BytesIO()
    Image.new("RGB", (3, 4)).save(output, format=format_)
    return base64.b64encode(output.getvalue()).decode()


def image_data_with_size(size):
    content = base64.b64decode(image_data())
    return base64.b64encode(content + b"\0" * (size - len(content))).decode()


@pytest.fixture
def data():
    return {
        "surname": "Иванов",
        "name": "Иван",
        "patronymic": "",
        "surname_genitive": "Иванова",
        "name_genitive": "Ивана",
        "patronymic_genitive": "",
        "citizenship": "РФ",
        "nationality": "Русский",
        "permanent_address": "",
        "marital_status": "Холост",
        "recruitment_office": "Военкомат Москвы",
        "birth_info": {"date": "2005-01-01", "country": "Россия", "place": "Москва"},
        "passport": {
            "series": "1234",
            "code": "123456",
            "ufms_code": "123-456",
            "ufms_name": "МВД",
            "issue_date": "2020-01-01",
        },
        "personal_documents_info": {
            "tax_id": "771234567890",
            "insurance_number": "123-456-789 00",
        },
        "university_info": {
            "campus": "MO",
            "program": 1,
            "card_id": "123",
            "group": "БИВ123",
            "graduation_year": 2029,
        },
        "contact_info": {
            "personal_email": "",
            "personal_phone_number": "",
            "corporate_email": "user@example.ru",
        },
        "family": [],
        "image": image_data(),
        "milspecialty": 1,
        "user": 1,
        "agreement": True,
        "isDataCorrect": True,
    }


def make_serializer(data, **kwargs):
    serializer = ApplicantMutateSerializer(data=data, **kwargs)
    faculty = Faculty(pk=1, campus="MO")
    program = Program(pk=1, faculty=faculty, available_to_choose_for_applicants=True)
    specialty = Milspecialty(pk=1, available_for=["MO"])
    specialty.is_selectable_by_program = Mock(return_value=True)
    serializer.fields["university_info"].fields["program"].queryset = Mock(
        get=Mock(return_value=program)
    )
    serializer.fields["milspecialty"].queryset = Mock(get=Mock(return_value=specialty))
    serializer.fields["user"].queryset = Mock(get=Mock(return_value=User(pk=1)))
    serializer.fields["user"].validators = []
    return serializer


def test_valid_questionnaire_and_non_hse_email(data):
    serializer = make_serializer(data)
    assert serializer.is_valid(), serializer.errors
    assert "campus" not in serializer.validated_data["university_info"]
    assert "agreement" not in serializer.validated_data
    assert "isDataCorrect" not in serializer.validated_data
    assert serializer.validated_data["marital_status"] == "SI"


@pytest.mark.parametrize(
    "field",
    [
        "birth_info",
        "passport",
        "personal_documents_info",
        "university_info",
        "contact_info",
        "image",
        "agreement",
        "isDataCorrect",
        "citizenship",
        "nationality",
        "marital_status",
    ],
)
def test_missing_required_fields_are_reported_in_russian(data, field):
    del data[field]
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    assert field in serializer.errors
    assert any("а" <= char.lower() <= "я" for char in str(serializer.errors[field]))


@pytest.mark.parametrize(
    "section,field,value",
    [
        (None, "name", "Иван123"),
        (None, "patronymic", "а" * 65),
        (None, "permanent_address", "а" * 129),
        (None, "marital_status", "UN"),
        (None, "agreement", False),
        (None, "isDataCorrect", False),
        ("birth_info", "date", "2023-02-29"),
        ("birth_info", "date", "2099-01-01"),
        ("birth_info", "country", " "),
        ("passport", "series", "abcd"),
        ("passport", "code", "123"),
        ("passport", "ufms_code", "1234567"),
        ("passport", "issue_date", "2099-01-01"),
        ("passport", "issue_date", "2000-01-01"),
        ("personal_documents_info", "tax_id", "a" * 12),
        ("personal_documents_info", "insurance_number", "12345678900"),
        ("university_info", "campus", "XX"),
        ("university_info", "campus", "PE"),
        ("university_info", "card_id", "а" * 33),
        ("university_info", "group", "а" * 33),
        ("university_info", "graduation_year", 29),
        ("university_info", "graduation_year", "2029abc"),
        ("contact_info", "personal_phone_number", "7abcdefghij"),
        ("contact_info", "personal_email", "@example.ru"),
    ],
)
def test_invalid_fields_have_structured_errors(data, section, field, value):
    target = data if section is None else data[section]
    target[field] = value
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    errors = serializer.errors if section is None else serializer.errors[section]
    expected_field = (
        "program" if section == "university_info" and value == "PE" else field
    )
    assert expected_field in errors


@pytest.mark.parametrize(
    "phone", ["+79001234567", "79001234567", "89001234567", " 89001234567 "]
)
def test_phone_normalization(data, phone):
    data["contact_info"]["personal_phone_number"] = phone
    serializer = make_serializer(data)
    assert serializer.is_valid(), serializer.errors
    assert (
        serializer.validated_data["contact_info"]["personal_phone_number"]
        == "79001234567"
    )


@pytest.mark.parametrize("name", ["Анна-Мария", "O’Connor", "李", "Де Ла Круз"])
def test_international_names(data, name):
    data["name"] = name
    serializer = make_serializer(data)
    assert serializer.is_valid(), serializer.errors


def test_every_relative_is_validated(data):
    relative = {
        "surname": "Иванов",
        "name": "Иван",
        "citizenship": "РФ",
        "permanent_address": "Москва",
        "birth_info": {"date": "1970-01-01", "country": "Россия", "place": "Москва"},
        "contact_info": {"personal_phone_number": "79001234567"},
    }
    data["family"] = [
        {**deepcopy(relative), "type": kind} for kind in ("MO", "FA", "BR", "BR", "SI")
    ]
    data["family"][1]["name"] = ""
    data["family"][3]["contact_info"]["personal_phone_number"] = "7abcdefghij"
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors["family"][1]
    assert "personal_phone_number" in serializer.errors["family"][3]["contact_info"]
    assert not serializer.errors["family"][0]


def test_parent_phone_error_has_relative_index(data):
    data["family"] = [
        {
            "type": "MO",
            "surname": "Иванова",
            "name": "Анна",
            "citizenship": "РФ",
            "permanent_address": "Москва",
            "birth_info": data["birth_info"],
            "contact_info": {},
        }
    ]
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    assert "personal_phone_number" in serializer.errors["family"][0]["contact_info"]


@pytest.mark.parametrize(
    "value", ["", {}, "data:;base64,foo;base64,bar", "not an image", image_data("GIF")]
)
def test_rejects_corrupt_or_unsupported_images(data, value):
    data["image"] = value
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    assert "image" in serializer.errors


def test_accepts_photo_at_2_mib_and_rejects_one_byte_over(data):
    data["image"] = image_data_with_size(MAX_PHOTO_SIZE_BYTES)
    serializer = make_serializer(data)
    assert serializer.is_valid(), serializer.errors

    data["image"] = image_data_with_size(MAX_PHOTO_SIZE_BYTES + 1)
    serializer = make_serializer(data)
    assert not serializer.is_valid()
    assert str(serializer.errors["image"][0]) == (
        "Размер фотографии не должен превышать 2 МБ"
    )


def test_unknown_specialty_is_a_field_error(data):
    serializer = make_serializer(data)
    serializer.fields[
        "milspecialty"
    ].queryset.get.side_effect = Milspecialty.DoesNotExist
    assert not serializer.is_valid()
    assert "milspecialty" in serializer.errors


def test_unavailable_specialty_is_a_field_error(data):
    serializer = make_serializer(data)
    serializer.fields[
        "milspecialty"
    ].queryset.get.return_value.is_selectable_by_program.return_value = False
    assert not serializer.is_valid()
    assert "milspecialty" in serializer.errors


def test_unavailable_program_is_a_field_error(data):
    serializer = make_serializer(data)
    serializer.fields["university_info"].fields[
        "program"
    ].queryset.get.return_value.available_to_choose_for_applicants = False
    assert not serializer.is_valid()
    assert "program" in serializer.errors["university_info"]


def test_partial_updates_check_dates_against_saved_birth_date():
    instance = Mock()
    instance.birth_info.date = date(2005, 1, 1)
    instance.passport.issue_date = date(2020, 1, 1)
    instance.university_info.program.faculty.campus = "MO"
    instance.milspecialty.available_for = ["MO"]
    serializer = make_serializer(
        {"passport": {"issue_date": "2000-01-01"}}, instance=instance, partial=True
    )
    assert not serializer.is_valid()
    assert "issue_date" in serializer.errors["passport"]
