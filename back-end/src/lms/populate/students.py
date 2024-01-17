from django.contrib.auth import get_user_model

from common.models.universities import (
    Program,
    UniversityInfo,
)
from common.models.personal import (
    ContactInfo,
    BirthInfo,
    Passport,
    PersonalDocumentsInfo,
    Relative,
)

from common.utils.populate import get_or_create

from lms.models.common import Milgroup
from lms.models.students import (
    Skill,
    Student,
)
from lms.populate.students_gen import get_students


User = get_user_model()


def create_skills() -> dict[str, Skill]:
    skills = [
        {
            "title": "Футбол",
        },
        {
            "title": "Гитара",
        },
        {
            "title": "Плавание",
        },
    ]

    return {fields["title"]: get_or_create(Skill, **fields) for fields in skills}


def create_students(
    users: dict[str, User],
    milgroups: dict[str, Milgroup],
    skills: dict[str, Skill],
    programs: dict[str, Program],
) -> dict[str, Student]:
    # TODO(TmLev): Provide `family` for some students.

    students = [
        {
            "surname": "Хромов",
            "name": "Григорий",
            "patronymic": "Александрович",
            "user": users["gakhromov@mail.com"],
            "milgroup": milgroups["1809"],
            "contact_info": {
                "personal_phone_number": "70000000001",
            },
            "status": Student.Status.STUDYING.value,
            "post": None,
            "skills": [skills["Футбол"], skills["Гитара"]],
            "photo": None,
            "birth_info": {
                "date": "2000-11-04",
                "country": "Россия",
                "place": "Москва",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Неглинка, дом 5",
            "passport": {
                "series": "0000",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567892",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП00",
                "card_id": "СТДБ00",
            },
            "family": [],
        },
        {
            "surname": "Кацевалов",
            "name": "Артем",
            "patronymic": "Сергеевич",
            "user": users["askatsevalov@mail.com"],
            "milgroup": milgroups["1809"],
            "contact_info": {
                "personal_phone_number": "70000000002",
            },
            "status": Student.Status.STUDYING.value,
            "post": Student.Post.MILGROUP_COMMANDER.value,
            "skills": [skills["Плавание"]],
            "photo": None,
            "birth_info": {
                "date": "2000-02-23",
                "country": "Россия",
                "place": "Томск",
            },
            "citizenship": "Подольск",
            "permanent_address": "г. Подольск, ул. Корабелов, дом 10",
            "passport": {
                "series": "1111",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567893",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП01",
                "card_id": "СТДБ01",
            },
            "family": [],
        },
        {
            "surname": "Исаков",
            "name": "Владислав",
            "patronymic": "Евгеньевич",
            "user": users["veisakov@mail.com"],
            "milgroup": milgroups["1809"],
            "contact_info": {
                "personal_phone_number": "70000000003",
            },
            "status": Student.Status.STUDYING.value,
            "post": Student.Post.MILSQUAD_COMMANDER.value,
            "skills": [skills["Футбол"], skills["Плавание"], skills["Гитара"]],
            "photo": None,
            "birth_info": {
                "date": "1999-08-29",
                "country": "Россия",
                "place": "Челябинск",
            },
            "passport": {
                "series": "2222",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234547890",
                "insurance_number": "200-200-200 20",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Волжский, ул. Плаксина, дом Какуна",
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП02",
                "card_id": "СТДБ02",
            },
            "family": [],
        },
        {
            "surname": "Алиев",
            "name": "Насир",
            "patronymic": "Ашурович",
            "user": users["naaliev@mail.com"],
            "milgroup": milgroups["1808"],
            "contact_info": {
                "personal_phone_number": "70000000004",
            },
            "status": Student.Status.STUDYING.value,
            "post": None,
            "skills": [skills["Футбол"], skills["Гитара"]],
            "photo": None,
            "birth_info": {
                "date": "1999-05-04",
                "country": "Россия",
                "place": "Махачкала",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Махачкала, ул. Ленина, дом 15",
            "passport": {
                "series": "3333",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567891",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП03",
                "card_id": "СТДБ03",
            },
            "family": [],
        },
        {
            "surname": "Куркин",
            "name": "Андрей",
            "patronymic": "Витальевич",
            "user": users["avkurkin@mail.com"],
            "milgroup": milgroups["1812"],
            "contact_info": {
                "personal_phone_number": "70000000005",
            },
            "status": Student.Status.STUDYING.value,
            "post": Student.Post.MILGROUP_COMMANDER.value,
            "skills": [skills["Плавание"], skills["Гитара"]],
            "photo": None,
            "birth_info": {
                "date": "1999-11-12",
                "country": "Россия",
                "place": "Тверь",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "passport": {
                "series": "4444",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567894",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП04",
                "card_id": "СТДБ04",
            },
            "family": [],
        },
        {
            "surname": "Иванов",
            "name": "Петр",
            "patronymic": "Сидорович",
            "user": users["psivanov@mail.com"],
            "milgroup": milgroups["1804"],
            "contact_info": {
                "personal_phone_number": "70000000006",
            },
            "status": Student.Status.EXPELLED.value,
            "post": Student.Post.MILSQUAD_COMMANDER.value,
            "skills": [skills["Гитара"]],
            "photo": None,
            "birth_info": {
                "date": "1999-05-04",
                "country": "Россия",
                "place": "Звенигород",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Ходынка, дом 9",
            "passport": {
                "series": "5555",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567895",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП05",
                "card_id": "СТДБ05",
            },
            "family": [],
        },
        {
            "surname": "Чукмарикадзе",
            "name": "Губарибек",
            "patronymic": "Алкинбеков",
            "user": None,
            "milgroup": milgroups["1612"],
            "contact_info": {
                "personal_phone_number": "70000000007",
            },
            "status": Student.Status.GRADUATED.value,
            "post": None,
            "skills": [],
            "photo": None,
            "birth_info": {
                "date": "1998-10-11",
                "country": "Россия",
                "place": "Сыктывкар",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Флотская, дом 6",
            "passport": {
                "series": "6666",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567896",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП06",
                "card_id": "СТДБ06",
            },
            "family": [],
        },
        {
            "surname": "Харламов",
            "name": "Денис",
            "patronymic": "",
            "user": None,
            "milgroup": milgroups["1612"],
            "contact_info": {
                "personal_phone_number": "70000000008",
            },
            "status": Student.Status.EXPELLED.value,
            "post": None,
            "skills": [],
            "photo": None,
            "birth_info": {
                "date": "1969-04-12",
                "country": "Швейцария",
                "place": "Цюрих",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Флотская, дом 6",
            "passport": {
                "series": "7777",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567897",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП07",
                "card_id": "СТДБ07",
            },
            "family": [],
        },
        {
            "surname": "Коронов",
            "name": "Илья",
            "patronymic": "Ахмат оглы",
            "user": None,
            "milgroup": milgroups["1612"],
            "contact_info": {
                "personal_phone_number": "70000000009",
            },
            "status": Student.Status.GRADUATED.value,
            "post": None,
            "skills": [],
            "photo": None,
            "birth_info": {
                "date": "1995-06-23",
                "country": "Россия",
                "place": "Владимир",
            },
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Ленина, дом 2",
            "passport": {
                "series": "8888",
                "code": "111111",
                "ufms_name": "УФМС гор. Москвы",
                "ufms_code": "740-056",
                "issue_date": "2020-10-02",
            },
            "personal_documents_info": {
                "tax_id": "771234567898",
                "insurance_number": "200-200-200 20",
            },
            "recruitment_office": "Московский военкомат",
            "university_info": {
                "program": programs["Информатика и вычислительная техника"],
                "group": "ГРПП08",
                "card_id": "СТДБ08",
            },
            "family": [],
        },
    ]

    students = students + get_students(users, milgroups, skills, programs)

    objects = {}

    for fields in students:
        existing_students_with_user = Student.objects.filter(user=fields["user"])
        if len(existing_students_with_user) > 0:
            objects[fields["surname"]] = existing_students_with_user.first()
            continue
        fields["contact_info"] = get_or_create(
            ContactInfo,
            **fields.pop("contact_info"),
        )
        fields["birth_info"] = get_or_create(
            BirthInfo,
            **fields.pop("birth_info"),
        )
        fields["passport"] = get_or_create(
            Passport,
            **fields.pop("passport"),
        )
        personal_documents_info = fields.pop("personal_documents_info", None)
        if personal_documents_info is not None:
            fields["personal_documents_info"] = get_or_create(
                PersonalDocumentsInfo,
                **personal_documents_info
            )

        fields["university_info"] = get_or_create(
            UniversityInfo,
            **fields.pop("university_info"),
        )

        skills = fields.pop("skills")
        family = [
            get_or_create(Relative, **relative_fields)
            for relative_fields in fields.pop("family")
        ]

        object_ = get_or_create(Student, **fields)

        object_.skills.add(*skills)
        object_.family.add(*family)
        object_.save()

        objects[fields["surname"]] = object_

    return objects
