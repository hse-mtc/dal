# User example populate
# Data(
#     email="superuser@mail.com",
#     password="qwerty",
#     is_staff=True,
#     is_superuser=True,
#     campuses=[Campus.MOSCOW.value],
# ),

# student example
# {
#     "surname": "Хромов",
#     "name": "Григорий",
#     "patronymic": "Александрович",
#     "user": users["gakhromov@mail.com"],
#     "milgroup": milgroups["1809"],
#     "contact_info": {
#         "personal_phone_number": "70000000001",
#     },
#     "status": Student.Status.STUDYING.value,
#     "post": None,
#     "skills": [skills["Футбол"], skills["Гитара"]],
#     "photo": None,
#     "birth_info": {
#         "date": "2000-11-04",
#         "country": "Россия",
#         "place": "Москва",
#     },
#     "citizenship": "РФ",
#     "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
#     "passport": {
#         "series": "0000",
#         "code": "111111",
#         "ufms_name": "УФМС гор. Москвы",
#         "ufms_code": "740-056",
#         "issue_date": "2020-10-02",
#     },
#     "recruitment_office": "Московский военкомат",
#     "university_info": {
#         "program": programs["Информатика и вычислительная техника"],
#         "group": "ГРПП00",
#         "card_id": "СТДБ00",
#     },
#     "family": [],
# },
from collections import namedtuple

Data = namedtuple(
    "Data",
    [
        "email",
        "password",
        "is_staff",
        "is_superuser",
        "campuses",
    ],
)


class Campus():
    MOSCOW = "MO", "Москва"
    SAINT_PETERSBURG = "SP", "Санкт-Петербург"
    NIZHNY_NOVGOROD = "NN", "Нижний Новгород"
    PERM = "PE", "Пермь"


# GLEB TODO: дополни список имен на русском и первую букву транслитом 
names = [('Алексей', 'a'), ('Борис', 'b'), ('Флекс', 'f'),]
# GLEB TODO: дополни список отчеств на русском и первую букву транслитом
patronymics = [('Алексеевич', 'a'), ('Флексеевич', 'f'),]
# GLEB TODO: дополни список фамилий на русском и транслите
surnames = [('Милос', 'milos'), ('Елочкин', 'elochkin'), ('Веточкин', 'vetochkin'),]

def create_email(name, surname, patronimic):
    return name + patronimic + surname + "@mail.com"


def create_milfaculties() -> dict[str]:
    milfaculties = [
        {
            "title": "Воздушно-космические силы",
            "abbreviation": "ВКС",
        },
        {
            "title": "Сержанты",
            "abbreviation": "Сержанты",
        },
        {
            "title": "Разведка",
            "abbreviation": "Разведка",
        },
        {
            "title": "Ракетные войска стратегического назначения",
            "abbreviation": "РВСН",
        },
    ]

    return {
        fields["abbreviation"]: ""
        for fields in milfaculties
    }


def create_milgroups(
    milfaculties: dict[str],
) -> dict[str]:
    milgroups = [
        {
            "title": "1801",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1802",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1803",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1804",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1805",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1806",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1807",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1808",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1809",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1810",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1811",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1812",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1612",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
    ]

    return {fields["title"]: "" for fields in milgroups}


def create_user(name, surname, patronimic) -> Data:
    return Data(
        email=create_email(name, surname, patronimic),
        password="qwerty",
        is_staff=True,
        is_superuser=False,
        campuses=[Campus.MOSCOW], # TODO: add .value
    )


def create_student() -> dict[str]:
    pass


milfaculties = create_milfaculties()
milgroups = create_milgroups(milfaculties)


print(create_user('абырвалг', 'хуй', 'хуевич'))
print(milfaculties)
print(milgroups)

for m_fac in milfaculties:
    for m_group in milgroups:
        pass
