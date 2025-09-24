import io

from conf.settings import TEST_CORPORATE_EMAIL_DOMAIN

from auth.models import User

from PIL import Image

from common.models.milspecialties import Milspecialty
from common.models.universities import (
    UniversityInfo,
    Program,
)
from common.models.personal import (
    BirthInfo,
    Passport,
    PersonalDocumentsInfo,
    ContactInfo,
    Relative,
    Photo,
)

from common.utils.populate import get_or_create

from ams.models.applicants import (
    ApplicationProcess,
    Applicant,
)

from django.core.files import File


def create_applicants(
    programs: dict[str, Program],
    milspecialties: dict[str, Milspecialty],
) -> dict[str, Applicant]:
    applicants = [
        # ----------------------------------------------------------------------
        # Campus == MO
        {
            "surname": "Иванов",
            "name": "Иван",
            "patronymic": "Иванович",
            "surname_genitive": "Иванова",
            "name_genitive": "Ивана",
            "patronymic_genitive": "Ивановича",
            "recruitment_office": "Московский военкомат",
            "citizenship": "РФ",
            "nationality": "Русский",
            "marital_status": "UN",
            "permanent_address": "г. Москва, ул. Тверская, д. 6",
            "birth_info": {
                "date": "2000-11-04",
                "country": "Россия",
                "place": "Москва",
            },
            "passport": {
                "series": "1000",
                "code": "222222",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567890",
                "insurance_number": "200-200-200 20",
            },
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП10",
                "card_id": "СТДБ10",
                "graduation_year": 2024,
            },
            "contact_info": {
                "corporate_email": f"ivanov@{TEST_CORPORATE_EMAIL_DOMAIN}",
                "personal_email": f"ivanov@ivanov.ru",
                "personal_phone_number": "72222222221",
            },
            "photo": 0,
            "family": [
                {
                    "surname": "Иванов",
                    "name": "Иван",
                    "patronymic": "Петрович",
                    "type": "FA",
                    "citizenship": "Россия",
                    "permanent_address": "Россия, Москва",
                    "birth_info": {
                        "date": "1960-12-05",
                        "country": "Россия",
                        "place": "Москва",
                    },
                },
                {
                    "surname": "Иванова",
                    "name": "Евгения",
                    "patronymic": "Сергеевна",
                    "type": "MO",
                    "citizenship": "Россия",
                    "permanent_address": "Россия, Москва",
                    "birth_info": {
                        "date": "1961-10-03",
                        "country": "Россия",
                        "place": "Москва",
                    },
                    "contact_info": {
                        "personal_email": f"ivanov@ivanov.ru",
                        "personal_phone_number": "72222222221",
                    },
                },
                {
                    "surname": "Иванов",
                    "name": "Евгений",
                    "patronymic": "Иванович",
                    "type": "BR",
                    "citizenship": "Россия",
                    "permanent_address": "Россия, Москва",
                    "birth_info": {
                        "date": "2005-01-09",
                        "country": "Россия",
                        "place": "Саратов",
                    },
                },
                {
                    "surname": "Иванова",
                    "name": "Елизавета",
                    "patronymic": "Ивановна",
                    "type": "SI",
                    "citizenship": "Россия",
                    "permanent_address": "Россия, Москва",
                    "birth_info": {
                        "date": "2009-02-10",
                        "country": "Россия",
                        "place": "Саратов",
                    },
                },
            ],
            # "application_process": {},
            "milspecialty": milspecialties["453100"],
            "user": User.objects.get(email=f"ivanov@{TEST_CORPORATE_EMAIL_DOMAIN}"),
        },
        # TODO(sha43): Add family for other applicants
        {
            "surname": "Петров",
            "name": "Иван",
            "patronymic": "Евгеньевич",
            "surname_genitive": "Петрова",
            "name_genitive": "Ивана",
            "patronymic_genitive": "Евгеньевича",
            "recruitment_office": "Московский военкомат",
            "citizenship": "РФ",
            "nationality": "Русский",
            "marital_status": "SI",
            "permanent_address": "г. Челябинск, ул. Ленина, д. 12",
            "birth_info": {
                "date": "2001-10-22",
                "country": "Россия",
                "place": "Москва",
            },
            "passport": {
                "series": "1001",
                "code": "222222",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234555890",
                "insurance_number": "200-200-200 20",
            },
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП11",
                "card_id": "СТДБ11",
                "graduation_year": 2024,
            },
            "contact_info": {
                "corporate_email": f"petrov@{TEST_CORPORATE_EMAIL_DOMAIN}",
                "personal_email": f"petrov@petrov.ru",
                "personal_phone_number": "72222222222",
            },
            "photo": 1,
            "family": [],
            # "application_process": {},
            "milspecialty": milspecialties["453100"],
            "user": User.objects.get(email=f"petrov@{TEST_CORPORATE_EMAIL_DOMAIN}"),
        },
        {
            "surname": "Сидоров",
            "name": "Николай",
            "patronymic": "Александрович",
            "surname_genitive": "Сидорова",
            "name_genitive": "Николая",
            "patronymic_genitive": "Александровича",
            "recruitment_office": "Объединённый Одинцовский военкомат",
            "citizenship": "Беларусь",
            "nationality": "Русский",
            "marital_status": "MA",
            "permanent_address": "г. Минск, ул. Картошки, д. Матрёшки",
            "birth_info": {
                "date": "1999-01-31",
                "country": "Беларусь",
                "place": "Минск",
            },
            "passport": {
                "series": "1002",
                "code": "222222",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "775534567890",
                "insurance_number": "200-200-200 20",
            },
            "university_info": {
                "program": programs["Экономика"],
                "group": "ГРПП12",
                "card_id": "СТДБ12",
                "graduation_year": 2023,
            },
            "contact_info": {
                "corporate_email": f"sidorov@{TEST_CORPORATE_EMAIL_DOMAIN}",
                "personal_email": f"sidorov@sidorov.ru",
                "personal_phone_number": "72222222223",
            },
            "photo": 2,
            "family": [],
            # "application_process": {},
            "milspecialty": milspecialties["453000"],
            "user": User.objects.get(email=f"sidorov@{TEST_CORPORATE_EMAIL_DOMAIN}"),
        },
        # ----------------------------------------------------------------------
        # Campus == SP
        {
            "surname": "Борисов",
            "name": "Никита",
            "patronymic": "Олегович",
            "surname_genitive": "Борисов",
            "name_genitive": "Никиты",
            "patronymic_genitive": "Олеговича",
            "recruitment_office": "Ленинградский военкомат",
            "citizenship": "РФ",
            "nationality": "Русский",
            "permanent_address": "г. Ульяновск, ул. Победы, д. Неведы",
            "birth_info": {
                "date": "2002-04-12",
                "country": "Россия",
                "place": "Санкт-Петербург",
            },
            "passport": {
                "series": "1003",
                "code": "222222",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "774334567890",
                "insurance_number": "200-200-200 20",
            },
            "university_info": {
                "program": programs["Юриспруденция"],
                "group": "ГРПП13",
                "card_id": "СТДБ13",
            },
            "contact_info": {
                "corporate_email": f"borisov@{TEST_CORPORATE_EMAIL_DOMAIN}",
                "personal_email": f"borisov@borisov.ru",
                "personal_phone_number": "72222222224",
            },
            "photo": 3,
            "family": [],
            # "application_process": {},
            "milspecialty": milspecialties["106646-543"],
            "user": User.objects.get(email=f"borisov@{TEST_CORPORATE_EMAIL_DOMAIN}"),
        },
        # ----------------------------------------------------------------------
        # Campus == NN
        # ----------------------------------------------------------------------
        # Campus == PE
    ]

    objects = {}

    photos = get_photos(4)

    for fields in applicants:
        assert _campus_matches(fields)

        fields["birth_info"] = get_or_create(
            BirthInfo,
            **fields.pop("birth_info"),
        )
        fields["passport"] = get_or_create(
            Passport,
            **fields.pop("passport"),
        )
        fields["personal_documents_info"] = get_or_create(
            PersonalDocumentsInfo, **fields.pop("personal_documents_info")
        )
        fields["university_info"] = get_or_create(
            UniversityInfo,
            **fields.pop("university_info"),
        )
        fields["contact_info"] = get_or_create(
            ContactInfo,
            **fields.pop("contact_info"),
        )
        fields["photo"] = photos[fields.pop("photo")]

        family = []
        for relative_fields in fields.pop("family"):
            relative_fields["birth_info"] = get_or_create(
                BirthInfo,
                **relative_fields.pop("birth_info"),
            )
            if "contact_info" in relative_fields:
                relative_fields["contact_info"] = get_or_create(
                    ContactInfo,
                    **relative_fields.pop("contact_info"),
                )
            family.append(get_or_create(Relative, **relative_fields))

        if "application_process" in fields:
            fields["application_process"] = get_or_create(
                ApplicationProcess,
                **fields.pop("application_process"),
            )
        if (
            queryset := Applicant.objects.filter(
                **{k: v for k, v in fields.items() if k != "photo"}
            )
        ).exists():
            object_ = queryset.first()
        else:
            object_ = Applicant.objects.create(**fields)

        object_.family.add(*family)
        object_.save()

        objects[fields["surname"]] = object_

    return objects


def get_photos(num_of_photos):
    photos = []
    for i in range(num_of_photos):
        image = Image.new("RGB", size=(1, 1))
        image.putpixel((0, 0), (0, 0, 0))
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        photo = Photo.objects.create(image=None)
        photo.image.save("Image.png", File(buf))
        photos.append(photo)
    return photos


def _campus_matches(fields) -> bool:
    program: Program = fields["university_info"]["program"]
    milspecialty: Milspecialty = fields["milspecialty"]
    return program.faculty.campus in milspecialty.available_for
