import base64

from django.utils import translation

from common.serializers.milspecialties import MilspecialtySerializer
from common.serializers.personal import (
    BirthInfoSerializer,
    ContactInfoSerializer,
    PassportSerializer,
    PersonalDocumentsInfoSerializer,
    PhotoMutateMixin,
    RelativeSerializer,
)
from common.serializers.universities import (
    UniversityInfoSerializer,
)
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from common.models.milspecialties import Milspecialty

from ams.models.applicants import (
    Applicant,
    ApplicationProcess,
)
from ams.serializers.physical import ExerciseResultSerializer
from ams.utils.common import get_current_admission_year

from ams.serializers.validation import (
    QuestionnaireFieldsMixin,
    ApplicantBirthSerializer,
    ApplicantContactSerializer,
    ApplicantPassportSerializer,
    ApplicantDocumentsSerializer,
    ApplicantUniversitySerializer,
    ApplicantRelativeSerializer,
    ApplicantImageField,
)


class ApplicationProcessSerializer(serializers.ModelSerializer):
    exercise_results = ExerciseResultSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationProcess
        exclude = ["id"]

    def create(self, validated_data):
        cur_adm_year = get_current_admission_year()
        validated_data["mtc_admission_year"] = validated_data.get(
            "mtc_admission_year", cur_adm_year
        )
        return super().create(validated_data)


class ApplicantSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    birth_info = BirthInfoSerializer(read_only=True)
    contact_info = ContactInfoSerializer(read_only=True)
    university_info = UniversityInfoSerializer(read_only=True)
    passport = PassportSerializer(read_only=True)
    personal_documents_info = PersonalDocumentsInfoSerializer(read_only=True)
    photo = serializers.SerializerMethodField(read_only=True)
    marital_status = serializers.SerializerMethodField(read_only=True)

    family = RelativeSerializer(read_only=True, many=True)

    milspecialty = MilspecialtySerializer(read_only=True)

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    def get_photo(self, obj: Applicant) -> str:
        return base64.b64encode(obj.photo.image.read()).decode()

    class Meta:
        model = Applicant
        exclude = ["id"]


class MaritalStatusField(serializers.ChoiceField):
    def to_internal_value(self, data):
        for key, display in self.choices.items():
            if display == data:
                return key
        return super().to_internal_value(data)


class ApplicantMutateSerializer(
    QuestionnaireFieldsMixin,
    WritableNestedModelSerializer,
    PhotoMutateMixin,
):
    birth_info = ApplicantBirthSerializer()
    passport = ApplicantPassportSerializer()
    personal_documents_info = ApplicantDocumentsSerializer()
    university_info = ApplicantUniversitySerializer()
    contact_info = ApplicantContactSerializer()
    family = ApplicantRelativeSerializer(required=False, many=True)
    image = ApplicantImageField(write_only=True, required=True)
    agreement = serializers.BooleanField(write_only=True)
    isDataCorrect = serializers.BooleanField(write_only=True)
    generate_documents = serializers.BooleanField(required=False, default=False)
    marital_status = MaritalStatusField(choices=Applicant.MaritalStatus.choices)
    required_fields = ("citizenship", "nationality", "marital_status")
    name_fields = (
        "surname",
        "name",
        "patronymic",
        "surname_genitive",
        "name_genitive",
        "patronymic_genitive",
    )

    def run_validation(self, data=serializers.empty):
        # Include built-in DRF errors (dates, email, lengths and foreign keys).
        with translation.override("ru"):
            return super().run_validation(data)

    def validate_marital_status(self, value):
        if value not in (
            Applicant.MaritalStatus.SINGLE,
            Applicant.MaritalStatus.MARRIED,
        ):
            raise serializers.ValidationError("Выберите семейное положение из списка")
        return value

    def validate(self, attrs):
        errors = {}
        for field in ("agreement", "isDataCorrect"):
            if field in attrs and attrs.pop(field) is not True:
                errors[field] = "Для отправки формы необходимо поставить галочку"
        birth = attrs.get("birth_info", {})
        passport = attrs.get("passport", {})
        birth_date = birth.get("date")
        issue_date = passport.get("issue_date")
        if self.instance:
            birth_date = birth_date or self.instance.birth_info.date
            issue_date = issue_date or self.instance.passport.issue_date
        if birth_date and issue_date and issue_date < birth_date:
            errors["passport"] = {
                "issue_date": "Дата выдачи паспорта не может быть раньше даты рождения"
            }
        family = attrs.get("family", [])
        parents = [
            i for i, member in enumerate(family) if member.get("type") in ("MO", "FA")
        ]
        if parents and not any(
            family[i].get("contact_info", {}).get("personal_phone_number")
            for i in parents
        ):
            family_errors = [{} for _ in family]
            family_errors[parents[0]] = {
                "contact_info": {
                    "personal_phone_number": "Укажите телефон хотя бы одного из родителей"
                }
            }
            errors["family"] = family_errors
        university = attrs.get("university_info", {})
        program = university.get("program")
        specialty = attrs.get("milspecialty")
        if self.instance:
            program = program or self.instance.university_info.program
            specialty = specialty or self.instance.milspecialty
        if (
            program
            and specialty
            and (
                program.faculty.campus not in specialty.available_for
                or not specialty.is_selectable_by_program(program)
            )
        ):
            errors[
                "milspecialty"
            ] = "Эта военная специальность недоступна для выбранной образовательной программы"
        if self.instance:
            email = attrs.get("contact_info", {}).get(
                "corporate_email", self.instance.contact_info.corporate_email
            )
            if email != self.instance.contact_info.corporate_email:
                errors["contact_info"] = {
                    "corporate_email": "Нельзя изменить email учётной записи через анкету"
                }
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

    class Meta:
        model = Applicant
        exclude = ["application_process"]

    def create(self, validated_data):
        self.create_photo(validated_data)
        return super().create(validated_data)

    def update(self, instance: Applicant, validated_data):
        self.update_photo(instance, validated_data)
        return super().update(instance, validated_data)


class ApplicantWithApplicationProcessSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(
        read_only=True,
        source="birth_info.date",
    )
    program_code = serializers.CharField(
        read_only=True,
        source="university_info.program.code",
    )
    program_id = serializers.IntegerField(
        read_only=True,
        source="university_info.program.id",
    )
    faculty = serializers.CharField(
        read_only=True,
        source="university_info.program.faculty.title",
    )
    milspecialty = MilspecialtySerializer(read_only=True)
    application_process = ApplicationProcessSerializer(read_only=True)
    marital_status = serializers.SerializerMethodField(read_only=True)

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    class Meta:
        model = Applicant
        fields = [
            "id",
            "fullname",
            "birth_date",
            "program_code",
            "program_id",
            "faculty",
            "milspecialty",
            "application_process",
            "marital_status",
        ]


class ApplicantMilspecialtyMutateSerializer(serializers.Serializer):
    """Смена ВУС абитуриента (лёгкий перенос без документов)."""

    milspecialty = serializers.PrimaryKeyRelatedField(
        queryset=Milspecialty.objects.all()
    )
