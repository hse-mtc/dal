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

import time
import random
from enum import Enum
from collections import namedtuple
from pathlib import Path


def str_time_prop(start, end, time_format, prop):
    """
    Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d", prop)


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


class Campus:
    MOSCOW = "MO", "Москва"
    SAINT_PETERSBURG = "SP", "Санкт-Петербург"
    NIZHNY_NOVGOROD = "NN", "Нижний Новгород"
    PERM = "PE", "Пермь"


names = [
    ("Алексей", "a"),
    ("Борис", "b"),
    ("Феликс", "f"),
    ("Павел", "p"),
    ("Александр", "a"),
    ("Дмитрий", "d"),
]
patronymics = [
    ("Алексеевич", "a"),
    ("Феликсович", "f"),
    ("Павлович", "p"),
    ("Александрович", "a"),
    ("Дмитриевич", "d"),
    ("Борисович", "b"),
]
surnames = [
    ("Ходилов", "hodilov"),
    ("Кретков", "kretkov"),
    ("Тишанов", "tishanov"),
    ("Закудряев", "zakudrjaev"),
    ("Демчин", "demchin"),
]
streets = [
    "Пушкина",
    "Электрозаводская",
    "Флотская",
    "Ботаническая",
    "Академика Королева",
    "Петровка",
    "Дмитровская",
    "Солнечная",
]
cities = [
    "Москва",
    "Санкт-Петербург",
    "Архангельск",
    "Астрахань",
    "Барнаул",
    "Белгород",
    "Биробиджан",
]


def create_email(name, surname, patronimic):
    return name + patronimic + surname + "@mail.com"


def create_milfaculties() -> dict[str]:
    _milfaculties = [
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
        {
            "title": "Офицеры ЗИТ",
            "abbreviation": "ЗИТ",
        },
        {
            "title": "Беспилотные летательные аппараты",
            "abbreviation": "БПЛА",
        },
    ]

    return {fields["abbreviation"]: "" for fields in _milfaculties}


def create_milgroups(
    milfaculties: dict[str],
) -> dict[str]:
    _milgroups = [
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
            "milfaculty": milfaculties["БПЛА"],
            "weekday": 4,
        },
        {
            "title": "1811",
            "milfaculty": milfaculties["БПЛА"],
            "weekday": 4,
        },
        {
            "title": "1812",
            "milfaculty": milfaculties["ЗИТ"],
            "weekday": 4,
        },
        {
            "title": "1813",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
        {
            "title": "1814",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
        {
            "title": "1614",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
    ]

    return {fields["title"]: "" for fields in _milgroups}


def create_skills() -> dict[str]:
    _skills = [
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

    return {fields["title"]: "" for fields in _skills}


def create_faculties() -> dict[str]:
    _faculties = [
        {
            "campus": Campus.MOSCOW,  # .value,
            "title": "Московский институт электроники и математики им. А.Н. Тихонова",
            "abbreviation": "МИЭМ",
        },
        {
            "campus": Campus.MOSCOW,  # .value,
            "title": "Факультет экономических наук",
            "abbreviation": "ФЭН",
        },
        {
            "campus": Campus.MOSCOW,  # .value,
            "title": "Факультет компьютерных наук",
            "abbreviation": "ФКН",
        },
        {
            "campus": Campus.SAINT_PETERSBURG,  # .value,
            "title": "Юридический факультет",
            "abbreviation": "ЮрФак",
        },
    ]

    return {fields["abbreviation"]: "" for fields in _faculties}


def create_programs(faculties: dict[str]) -> dict[str]:
    _programs = [
        {
            "code": "09.03.01 Информатика и вычислительная техника",
            "title": "Информатика и вычислительная техника",
            "faculty": faculties["МИЭМ"],
        },
        {
            "code": "10.03.01 Информационная безопасность",
            "title": "Информационная безопасность",
            "faculty": faculties["МИЭМ"],
        },
        {
            "code": "38.03.01 Экономика",
            "title": "Экономика",
            "faculty": faculties["ФКН"],
        },
        {
            "code": "09.03.04 Программная инженерия",
            "title": "Программная инженерия",
            "faculty": faculties["ФКН"],
        },
        {
            "code": "40.03.01 Юриспруденция",
            "title": "Юриспруденция",
            "faculty": faculties["ЮрФак"],
        },
    ]

    return {fields["title"]: "" for fields in _programs}


def create_user(name, surname, patronimic) -> Data:
    return Data(
        email=create_email(name, surname, patronimic),
        password="qwerty",
        is_staff=False,
        is_superuser=False,
        campuses=[Campus.MOSCOW],  # TODO: add .value
    )


def generate_phone():
    generate_phone.last_phone += 1
    return generate_phone.last_phone


def generate_permanent_adress():
    city = random.choice(cities)
    _street = random.choice(streets)
    house = random.randint(1, 100)
    return f"г. {city}, ул. {_street}, дом {house}", city


class Posts(Enum):
    NO_POST = "None"
    MILGROUP_COMMANDER = "Student.Post.MILGROUP_COMMANDER.value"
    MILSQUAD_COMMANDER = "Student.Post.MILSQUAD_COMMANDER.value"


def generate_post(post: Posts):
    return f"""{post.value}"""


def generate_skills(skills: dict):
    _skills = []

    values = set(skills.keys())
    skills_count = random.randint(0, len(values))

    for i in range(skills_count):
        value = random.choice(list(values))
        _skills.append(value)
        values.remove(value)

    result = ""
    for i, s in enumerate(_skills):
        if i < len(_skills) - 1:
            result += """skills["{}"], """.format(s)
        else:
            result += """skills["{}"]""".format(s)
    return f"""{result}"""


def generate_birth_info():
    date = random_date("2000-1-1", "2000-12-31", random.random())
    return """{{
            "date": "{}",
            "country": "Россия",
            "place": "Москва",
        }}""".format(
        date
    )


def generate_passport(city):
    generate_passport.series += 1
    generate_passport.number += 1
    return """{{
            "series": "{}",
            "code": "{}",
            "ufms_name": "УФМС гор. {}",
            "ufms_code": "740-056",
            "issue_date": "2020-10-02",
            "tax_id": "771234567890",
            "insurance_number": "200-200-200 20",
        }}""".format(
        generate_passport.series, generate_passport.number, city
    )


def generate_university_info(programs):
    generate_university_info.group += 1
    generate_university_info.card_id += 1

    return """{{
                "program": programs["{}"],
                "group": "ГРПП{}",
                "card_id": "СТДБ{}",
            }}""".format(
        random.choice(list(programs.keys())),
        generate_university_info.group,
        generate_university_info.card_id,
    )


def generate_student(args):
    """
    args: surname, name, patronymic, mail,
    milgroup, phone, post, skills, birth_info,
    adress, passport, university info
    """
    return """{{
        "surname": "{}",
        "name": "{}",
        "patronymic": "{}",
        "user": users["{}"],
        "milgroup": milgroups["{}"],
        "contact_info": {{
            "personal_phone_number": "{}",
        }},
        "status": Student.Status.STUDYING.value,
        "post": {},
        "skills": [{}],
        "photo": None,
        "birth_info": {},
        "citizenship": "РФ",
        "permanent_address": "{}",
        "passport": {},
        "recruitment_office": "Московский военкомат",
        "university_info": {},
        "family": [],
    }},""".format(
        *args
    )


milfaculties = create_milfaculties()
milgroups = create_milgroups(milfaculties)
skills = create_skills()
faculties = create_faculties()
programs = create_programs(faculties)
posts = [Posts.NO_POST, Posts.MILGROUP_COMMANDER, Posts.MILSQUAD_COMMANDER]


generate_phone.last_phone = 79850000002
generate_passport.series = 1111
generate_passport.number = 111111

generate_university_info.group = 0
generate_university_info.card_id = 0

STUDENTS_HEADER = """from lms.models.students import Student


def get_students(users, milgroups, skills, programs):
    return [
"""

STUDENTS_FOOTER = "]"

USERS_HEADER = """from collections import namedtuple

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


def get_users():
    return [
"""

USERS_FOOTER = "]"


def generate():
    users_list = []
    milgroup_students_count = 3
    with open(Path(__file__).parent.parent / "./students_gen.py", "w") as students:

        print(STUDENTS_HEADER, file=students)
        for m_group in milgroups:
            gc, sc = random.sample(list(range(milgroup_students_count)), 2)

            for j in range(milgroup_students_count):
                name = random.choice(names)
                surname = random.choice(surnames)
                patronymic = random.choice(patronymics)
                user = create_user(name[1], surname[1], patronymic[1])

                while user in users_list:
                    name = random.choice(names)
                    surname = random.choice(surnames)
                    patronymic = random.choice(patronymics)
                    user = create_user(name[1], surname[1], patronymic[1])

                users_list.append(user)

                if j == gc:
                    post = Posts.MILGROUP_COMMANDER
                elif j == sc:
                    post = Posts.MILSQUAD_COMMANDER
                else:
                    post = Posts.NO_POST

                permanent_adress, city = generate_permanent_adress()
                print(
                    generate_student(
                        [
                            surname[0],
                            name[0],
                            patronymic[0],
                            user.email,
                            m_group,
                            generate_phone(),
                            generate_post(post),
                            generate_skills(skills),
                            generate_birth_info(),
                            permanent_adress,
                            generate_passport(city),
                            generate_university_info(programs),
                        ]
                    ),
                    file=students,
                )

        print(STUDENTS_FOOTER, file=students)

    with open(
        Path(__file__).parent.parent.parent.parent / "./auth/populate/users_gen.py", "w"
    ) as users:
        print(USERS_HEADER, file=users)
        for user in users_list:
            print(str(user) + ",", file=users)
        print(USERS_FOOTER, file=users)


generate()
