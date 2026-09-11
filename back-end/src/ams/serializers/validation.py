"""Validation for the applicant questionnaire (without changing student forms)."""

import re
import unicodedata

from django.utils import timezone
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from common.models.universities import Campus
from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PassportSerializer,
    PersonalDocumentsInfoSerializer,
    RelativeMutateSerializer,
)
from common.serializers.universities import UniversityInfoMutateSerializer

MAX_PHOTO_SIZE_BYTES = 2 * 1024 * 1024


def validate_name(value):
    parts = re.split(r"[ '\u2019-]", value)
    if not all(
        part and all(unicodedata.category(char)[0] in "LM" for char in part)
        for part in parts
    ):
        raise serializers.ValidationError(
            "Используйте буквы; между частями имени допустимы пробел, дефис или апостроф"
        )


def not_future(value):
    if value > timezone.localdate():
        raise serializers.ValidationError("Дата не может быть в будущем")


def formatted(pattern, message):
    def validate(value):
        if not re.fullmatch(pattern, value, flags=re.ASCII):
            raise serializers.ValidationError(message)

    return validate


class ApplicantImageField(Base64ImageField):
    ALLOWED_TYPES = ("jpg", "jpeg", "png")
    INVALID_FILE_MESSAGE = (
        "Не удалось прочитать фотографию. Загрузите исправный файл JPG или PNG"
    )
    INVALID_TYPE_MESSAGE = "Загрузите фотографию в формате JPG или PNG"

    def to_internal_value(self, data):
        if not isinstance(data, str) or not data.strip():
            raise serializers.ValidationError(self.INVALID_FILE_MESSAGE)
        try:
            image = super().to_internal_value(data)
        except (ValueError, TypeError):
            raise serializers.ValidationError(self.INVALID_FILE_MESSAGE)
        if image.size > MAX_PHOTO_SIZE_BYTES:
            raise serializers.ValidationError(
                "Размер фотографии не должен превышать 2 МБ"
            )
        return image


class QuestionnaireFieldsMixin:
    required_fields = ()
    name_fields = ()

    def get_fields(self):
        fields = super().get_fields()
        for name in self.required_fields:
            field = fields[name]
            field.required = True
            field.allow_null = False
            if hasattr(field, "allow_blank"):
                field.allow_blank = False
            field.default = serializers.empty
        for name in self.name_fields:
            fields[name].validators.append(validate_name)
        return fields


class ApplicantBirthSerializer(QuestionnaireFieldsMixin, BirthInfoSerializer):
    required_fields = ("date", "country", "place")

    def validate_date(self, value):
        not_future(value)
        return value


class ApplicantContactSerializer(ContactInfoSerializer):
    def validate_personal_phone_number(self, value):
        if not value:
            return value
        formatted(
            r"(?:\+7|7|8)\d{10}",
            "Введите 11 цифр телефона, начиная с 7 или 8; также можно указать +7",
        )(value)
        return "7" + value.lstrip("+")[1:]


class ApplicantPassportSerializer(PassportSerializer):
    def validate_series(self, value):
        formatted(r"\d{4}", "Введите 4 цифры серии паспорта")(value)
        return value

    def validate_code(self, value):
        formatted(r"\d{6}", "Введите 6 цифр номера паспорта")(value)
        return value

    def validate_ufms_code(self, value):
        formatted(r"\d{3}-\d{3}", "Введите код подразделения в формате 123-456")(value)
        return value

    def validate_issue_date(self, value):
        not_future(value)
        return value


class ApplicantDocumentsSerializer(PersonalDocumentsInfoSerializer):
    def validate_tax_id(self, value):
        formatted(r"\d{12}", "Введите 12 цифр ИНН")(value)
        return value

    def validate_insurance_number(self, value):
        formatted(r"\d{3}-\d{3}-\d{3} \d{2}", "Введите СНИЛС в формате 123-456-789 00")(
            value
        )
        return value


class ApplicantUniversitySerializer(
    QuestionnaireFieldsMixin, UniversityInfoMutateSerializer
):
    campus = serializers.ChoiceField(choices=Campus.choices, write_only=True)
    required_fields = ("graduation_year",)

    def validate_graduation_year(self, value):
        if not 1000 <= value <= 9999:
            raise serializers.ValidationError("Введите год из 4 цифр, например 2029")
        return value

    def validate(self, attrs):
        program = attrs.get("program")
        campus = attrs.pop("campus", None)
        if program:
            if campus and campus != program.faculty.campus:
                raise serializers.ValidationError(
                    {
                        "program": "Образовательная программа не относится к выбранному кампусу"
                    }
                )
            if not program.available_to_choose_for_applicants:
                raise serializers.ValidationError(
                    {
                        "program": "Эта образовательная программа недоступна для поступления"
                    }
                )
        return super().validate(attrs)


class ApplicantRelativeSerializer(QuestionnaireFieldsMixin, RelativeMutateSerializer):
    birth_info = ApplicantBirthSerializer()
    contact_info = ApplicantContactSerializer()
    required_fields = ("citizenship", "permanent_address")
    name_fields = ("surname", "name", "patronymic")
