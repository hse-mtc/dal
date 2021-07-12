# pylint: disable=line-too-long,unused-argument,too-many-arguments,too-many-locals

from datetime import (
    datetime,
    timedelta,
    time,
)

from django.contrib.auth import get_user_model

from common.models.persons import BirthInfo

from lms.models.common import (
    Milfaculty,
    Milgroup,
    Milspecialty,
)
from lms.models.universities import (
    Faculty,
    Program,
    UniversityInfo,
)
from lms.models.students import (
    Student,
    Passport,
    RecruitmentOffice,
    Skill,
)
from lms.models.teachers import (
    Rank,
    Teacher,
)
from lms.models.absences import (
    Absence,
    AbsenceTime,
)
from lms.models.encouragements import Encouragement
from lms.models.punishments import Punishment
from lms.models.achievements import (
    AchievementType,
    Achievement,
)
from lms.models.lessons import (
    Room,
    Lesson,
)
from lms.models.marks import Mark
from lms.models.uniforms import Uniform

from common.models.subjects import Subject
from common.models.persons import ContactInfo


User = get_user_model()

# ------------------------------------------------------------------------------
# Universities

def create_faculties():
    values = ["МИЭМ", "МИЭФ", "ФКН"]

    faculties = {}

    for value in values:
        faculty, _ = Faculty.objects.get_or_create(title=value)
        faculty.save()
        faculties[value] = faculty

    return faculties


def create_programs(faculties: dict[str, Faculty]) -> dict[str, Program]:
    values = [{
        "code": "09.03.01",
        "title": "Информатика и вычислительная техника",
        "faculty": faculties["МИЭМ"],
    }, {
        "code": "09.03.04",
        "title": "Программная инженерия",
        "faculty": faculties["ФКН"],
    }, {
        "code": "15.03.01",
        "title": "Машиностроение",
        "faculty": faculties["МИЭМ"],
    }, {
        "code": "45.03.04",
        "title": "Интеллектуальные системы в гуманитарной сфере",
        "faculty": faculties["МИЭМ"],
    }]

    programs = {}

    for value in values:
        program, _ = Program.objects.get_or_create(**value)
        program.save()
        programs[value["title"]] = program

    return programs


def create_university_infos(
    programs: dict[str, Program],
) -> dict[str, UniversityInfo]:
    values = [{
        "card_id": "HSE11229",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.MOSCOW.value,
    }, {
        "card_id": "HSE1129",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.MOSCOW.value,
    }, {
        "card_id": "HSE11319",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.MOSCOW.value,
    }, {
        "card_id": "HSE1889",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.PERM.value,
    }, {
        "card_id": "HSE11255",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.NIZHNY_NOVGOROD.value,
    }, {
        "card_id": "HSE1199",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.SAINT_PETERSBURG.value,
    }, {
        "card_id": "HSE7779",
        "group": "БИТ 188",
        "program": programs["Информатика и вычислительная техника"],
        "campus": UniversityInfo.Campus.MOSCOW.value,
    }]

    infos = {}

    for fields in values:
        info, _ = UniversityInfo.objects.get_or_create(**fields)
        infos[fields["card_id"]] = info

    return infos

# ------------------------------------------------------------------------------
# LMS.Common


def create_milfaculties() -> dict[str, Milfaculty]:
    values = [{
        "title": "Воздушно-космические силы",
        "abbreviation": "ВКС",
    }, {
        "title": "Сержанты",
        "abbreviation": "Сержанты",
    }, {
        "title": "Разведка",
        "abbreviation": "Разведка",
    }, {
        "title": "Ракетные войска стратегического назначения",
        "abbreviation": "РВСН",
    }]

    milfaculties = {}

    for value in values:
        milfaculty, _ = Milfaculty.objects.get_or_create(**value)
        milfaculty.save()
        milfaculties[value["abbreviation"]] = milfaculty

    return milfaculties


def create_milgroups(
    milfaculties: dict[str, Milfaculty],
) -> dict[str, Milgroup]:
    values = [{
        "title": "1801",
        "milfaculty": milfaculties["Разведка"],
        "weekday": 4,
    }, {
        "title": "1802",
        "milfaculty": milfaculties["Разведка"],
        "weekday": 4,
    }, {
        "title": "1803",
        "milfaculty": milfaculties["Разведка"],
        "weekday": 4,
    }, {
        "title": "1804",
        "milfaculty": milfaculties["Сержанты"],
        "weekday": 4,
    }, {
        "title": "1805",
        "milfaculty": milfaculties["Сержанты"],
        "weekday": 4,
    }, {
        "title": "1806",
        "milfaculty": milfaculties["Сержанты"],
        "weekday": 4,
    }, {
        "title": "1807",
        "milfaculty": milfaculties["ВКС"],
        "weekday": 4,
    }, {
        "title": "1808",
        "milfaculty": milfaculties["ВКС"],
        "weekday": 4,
    }, {
        "title": "1809",
        "milfaculty": milfaculties["ВКС"],
        "weekday": 4,
    }, {
        "title": "1810",
        "milfaculty": milfaculties["РВСН"],
        "weekday": 4,
    }, {
        "title": "1811",
        "milfaculty": milfaculties["РВСН"],
        "weekday": 4,
    }, {
        "title": "1812",
        "milfaculty": milfaculties["РВСН"],
        "weekday": 4,
    }]

    milgroups = {}

    for value in values:
        milgroup, _ = Milgroup.objects.get_or_create(**value)
        milgroup.save()
        milgroups[value["title"]] = milgroup

    return milgroups


def create_milspecialties():
    values = [{
        "code": "453000",
        "title": "Организация эксплуатации и ремонта автоматизированных "
                 "систем управления и вычислительных комплексов "
                 "ракетно-космической обороны",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "453100",
        "title":
            "Математическое и программное обеспечение функционирования "
            "вычислительных комплексов ракетно-космической обороны",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "461300",
        "title": "Эксплуатация и ремонт радиоэлектронного оборудования "
                        "самолетов, вертолетов и авиационных ракет",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "094001",
        "title": "Применение наземных подразделений войсковой разведки",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "411300",
        "title": "Эксплуатация и ремонт автоматизированных систем "
                        "комплексов баллистических стратегических ракет "
                        "наземного базирования",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "751100",
        "title": "Защита информационных технологий",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "100182",
        "title": "Стрелковые, командир стрелкового отделения",
        "available_for": [UniversityInfo.Campus.MOSCOW.value],
    }, {
        "code": "106646-543",
        "title": "Разведывательные, разведчик-оператор СБР, ПСНР",
        "available_for": UniversityInfo.Campus.values,
    }]

    specs = {}

    for value in values:
        spec, _ = Milspecialty.objects.get_or_create(**value)
        spec.save()
        specs[value["title"]] = spec

    return specs

# ------------------------------------------------------------------------------
# Teachers


def create_ranks() -> dict[str, Rank]:
    values = ["Подполковник", "Полковник", "Майор", "Генерал-майор"]

    ranks = {}

    for value in values:
        rank, _ = Rank.objects.get_or_create(title=value)
        rank.save()
        ranks[value] = rank

    return ranks


def create_teachers(
    milgroups: dict[str, Milgroup],
    milfaculties: dict[str, Milfaculty],
    ranks: dict[str, Rank],
    users: dict[str, User],
):
    values = [
        {
            "surname": "Никандров",
            "name": "Игорь",
            "patronymic": "Владимирович",
            "milfaculty": milfaculties["ВКС"],
            "rank": ranks["Подполковник"],
            "post": Teacher.Post.TEACHERS.value,
            "milgroups": [milgroups["1809"]],
            "user": users["ivnikandrov@mail.com"],
        },
        {
            "surname": "Репалов",
            "name": "Дмитрий",
            "patronymic": "Николаевич",
            "milfaculty": milfaculties["ВКС"],
            "rank": ranks["Подполковник"],
            "post": Teacher.Post.MILFACULTY_HEAD.value,
            "milgroups": [milgroups["1808"], milgroups["1809"]],
            "user": users["dnrepalov@mail.com"],
        },
        {
            "surname": "Мещеряков",
            "name": "Иван",
            "patronymic": "Владимирович",
            "milfaculty": milfaculties["Сержанты"],
            "rank": ranks["Майор"],
            "post": Teacher.Post.TEACHERS.value,
            "milgroups": [milgroups["1806"]],
            "user": users["ivmesheryakov@mail.com"],
        },
        {
            "surname": "Ковальчук",
            "name": "Игорь",
            "patronymic": "Валентинович",
            "milfaculty": milfaculties["Разведка"],
            "rank": ranks["Полковник"],
            "post": Teacher.Post.MILFACULTY_HEAD.value,
            "milgroups": [milgroups["1801"]],
            "user": users["ivkovalchuk@mail.com"],
        },
        {
            "surname": "Гаврилов",
            "name": "Климент",
            "patronymic": "Сергеевич",
            "milfaculty": milfaculties["РВСН"],
            "rank": ranks["Генерал-майор"],
            "post": Teacher.Post.TEACHERS.value,
            "milgroups": None,
            "user": users["ksgavrilov@mail.com"],
        },
    ]

    teachers = {}

    for value in values:
        milgroups = value.pop("milgroups")
        teacher, _ = Teacher.objects.get_or_create(**value)
        if milgroups:
            teacher.milgroups.add(*milgroups)
        teacher.save()
        teachers[value["surname"]] = teacher

    return teachers

# ------------------------------------------------------------------------------
# Applicants


def create_passports() -> dict[str, Passport]:
    values = [{
        "series": "0000",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "1111",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "2222",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "3333",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "4444",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "5555",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "6666",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "7777",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }, {
        "series": "8888",
        "code": "111111",
        "ufms_name": "УФМС гор. Москвы",
        "ufms_code": "740-056",
        "issue_date": "2020-10-02",
    }]

    passports = {}

    for fields in values:
        passport, _ = Passport.objects.get_or_create(**fields)
        passports[fields["series"]] = passport

    return passports


def create_recruitments_offices() -> dict[str, RecruitmentOffice]:
    values = [{
        "title": "городов Одинцово, Звенигород, Краснознаменск и "
                 "Одинцовского городского округа",
        "city": "Одинцово",
        "district": "Одинцовский",
    }, {
        "title": "Московский военкомат",
        "city": "Москва",
        "district": "ЦАО",
    }]

    offices = {}

    for fields in values:
        office, _ = RecruitmentOffice.objects.get_or_create(**fields)
        offices[fields["city"]] = office

    return offices

# ------------------------------------------------------------------------------
# Common


def create_contact_infos() -> dict[str, ContactInfo]:
    values = [{
        "personal_phone_number": "79608956420",
    }, {
        "personal_phone_number": "78005553535"
    }]

    contacts = {}

    for value in values:
        contact, _ = ContactInfo.objects.get_or_create(**value)
        contact.save()
        contacts[value["personal_phone_number"]] = contact

    return contacts


def create_birth_infos() -> dict[str, BirthInfo]:
    values = [{
        "date": "2000-11-04",
        "country": "Россия",
        "city": "Москва",
    }, {
        "date": "2000-02-23",
        "country": "Украина",
        "city": "Донбасс",
    }, {
        "date": "1999-08-29",
        "country": "Россия",
        "city": "Челябинск",
    }, {
        "date": "1999-05-14",
        "country": "Дагестан",
        "city": "Махачкала",
    }, {
        "date": "1999-11-12",
        "country": "Россия",
        "city": "Тверь",
    }, {
        "date": "1999-05-04",
        "country": "Литва",
        "city": "Литвения",
    }, {
        "date": "1969-04-13",
        "country": "Швейцария",
        "city": "Цюрих",
    }]

    infos = {}

    for value in values:
        info, _ = BirthInfo.objects.get_or_create(**value)
        info.save()
        infos[value["date"]] = info

    return infos


# ------------------------------------------------------------------------------
# Students


def create_skills() -> dict[str, Skill]:
    values = ["Футбол", "Гитара", "Кац"]

    skills = {}

    for value in values:
        skill, _ = Skill.objects.get_or_create(title=value)
        skill.save()
        skills[value] = skill

    return skills


def create_students(
    milgroups: dict[str, Milgroup],
    milspecialties: dict[str, Milspecialty],
    passports: dict[str, Passport],
    recruitment_offices: dict[str, RecruitmentOffice],
    university_infos: dict[str, UniversityInfo],
    skills: dict[str, Skill],
    contact_infos: dict[str, ContactInfo],
    birth_infos: dict[str, BirthInfo],
    users: dict[str, User],
):
    # TODO – index term
    # FIXME(TmLev): provide family for every student

    values = [
        {
            "surname": "Хромов",
            "name": "Григорий",
            "patronymic": "Александрович",
            "milgroup": milgroups["1809"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["2000-11-04"],
            "status": Student.Status.STUDENT.value,
            "photo": None,
            "surname_genitive": "Хромова",
            "name_genitive": "Григория",
            "patronymic_genitive": "Александровича",
            "passport": passports["0000"],
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE11229"],
            "post": None,
            "contact_info": contact_infos["78005553535"],
            "skills": [skills["Футбол"], skills["Гитара"]],
            "user": users["gakhromov@mail.com"],
        },
        {
            "surname": "Кацевалов",
            "name": "Артем",
            "patronymic": "Сергеевич",
            "milgroup": milgroups["1809"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["2000-02-23"],
            "status": Student.Status.STUDENT.value,
            "photo": None,
            "surname_genitive": "Кацевалова",
            "name_genitive": "Артема",
            "patronymic_genitive": "Сергеевича",
            "passport": passports["1111"],
            "citizenship": "Подольск",
            "permanent_address": "г. Подольск, ул. Кац, дом Цак",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE1129"],
            "post": Student.Post.MILGROUP_COMMANDER.value,
            "contact_info": contact_infos["78005553535"],
            "skills": [skills["Кац"]],
            "user": users["askatsevalov@mail.com"],
        },
        {
            "surname": "Исаков",
            "name": "Владислав",
            "patronymic": "Евгеньевич",
            "milgroup": milgroups["1809"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1999-08-29"],
            "status": Student.Status.STUDENT.value,
            "photo": None,
            "surname_genitive": "Исакова",
            "name_genitive": "Владислава",
            "patronymic_genitive": "Евгеньевича",
            "passport": passports["2222"],
            "citizenship": "РФ",
            "permanent_address": "г. Волжский, ул. Плаксина, дом Какуна",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE11319"],
            "post": Student.Post.MILSQUAD_COMMANDER.value,
            "contact_info": contact_infos["79608956420"],
            "skills": [skills["Футбол"], skills["Кац"], skills["Гитара"]],
            "user": users["veisakov@mail.com"],
        },
        {
            "surname": "Алиев",
            "name": "Насир",
            "patronymic": "Ашурович",
            "milgroup": milgroups["1808"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1999-05-14"],
            "status": Student.Status.STUDENT.value,
            "photo": None,
            "surname_genitive": "Алиева",
            "name_genitive": "Насира",
            "patronymic_genitive": "Ашуровича",
            "passport": passports["3333"],
            "citizenship": "Дагестан",
            "permanent_address": "г. Махачкала, ул. Рамзана Кадырова, дом 228",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE1889"],
            "post": None,
            "contact_info": contact_infos["78005553535"],
            "skills": [skills["Футбол"], skills["Гитара"]],
            "user": users["naaliev@mail.com"],
        },
        {
            "surname": "Куркин",
            "name": "Андрей",
            "patronymic": "Витальевич",
            "milgroup": milgroups["1812"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1999-11-12"],
            "status": Student.Status.STUDENT.value,
            "photo": None,
            "surname_genitive": "Куркина",
            "name_genitive": "Андрея",
            "patronymic_genitive": "Витальевича",
            "passport": passports["4444"],
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE11255"],
            "post": Student.Post.MILGROUP_COMMANDER.value,
            "contact_info": contact_infos["78005553535"],
            "skills": [skills["Кац"], skills["Гитара"]],
            "user": users["avkurkin@mail.com"],
        },
        {
            "surname": "Иванов",
            "name": "Петр",
            "patronymic": "Сидорович",
            "milgroup": milgroups["1804"],
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1999-05-04"],
            "status": Student.Status.EXPELLED.value,
            "photo": None,
            "surname_genitive": "Иванова",
            "name_genitive": "Петра",
            "patronymic_genitive": "Сидоровича",
            "passport": passports["5555"],
            "citizenship": "РФ",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE1199"],
            "post": Student.Post.MILSQUAD_COMMANDER.value,
            "contact_info": contact_infos["78005553535"],
            "skills": [skills["Гитара"]],
            "user": users["psivanov@mail.com"],
        },
        {
            "surname": "Чукмарикадзе",
            "name": "Губарибек",
            "patronymic": "Алкинбеков",
            "milgroup": None,
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1969-04-13"],
            "status": Student.Status.APPLICANT.value,
            "photo": None,
            "surname_genitive": "Чукмаридзе",
            "name_genitive": "Губарибека",
            "patronymic_genitive": "Алкинбекова",
            "passport": passports["6666"],
            "citizenship": "Узбекистан",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE7779"],
            "post": None,
            "contact_info": contact_infos["78005553535"],
            "skills": [],
            "user": None,
        },
        {
            "surname": "Харламов",
            "name": "Денис",
            "patronymic": "",
            "milgroup": None,
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1969-04-13"],
            "status": Student.Status.APPLICANT.value,
            "photo": None,
            "surname_genitive": "Харламова",
            "name_genitive": "Дениса",
            "patronymic_genitive": "",
            "passport": passports["7777"],
            "citizenship": "Узбекистан",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE7779"],
            "post": None,
            "contact_info": contact_infos["78005553535"],
            "skills": [],
            "user": None,
        },
        {
            "surname": "Силуанов",
            "name": "Илья",
            "patronymic": "Ахмат оглы",
            "milgroup": None,
            "milspecialty": milspecialties["Защита информационных технологий"],
            "birth_info": birth_infos["1969-04-13"],
            "status": Student.Status.APPLICANT.value,
            "photo": None,
            "surname_genitive": "Силуанова",
            "name_genitive": "Ильи",
            "patronymic_genitive": "Ахмат оглы",
            "passport": passports["8888"],
            "citizenship": "Узбекистан",
            "permanent_address": "г. Москва, ул. Пупкина, дом Кукушкина",
            "recruitment_office": recruitment_offices["Москва"],
            "university_info": university_infos["HSE7779"],
            "post": None,
            "contact_info": contact_infos["78005553535"],
            "skills": [],
            "user": None,
        },
    ]

    students = {}

    for fields in values:
        skills = fields.pop("skills")
        student, _ = Student.objects.get_or_create(**fields)
        student.skills.add(*skills)
        student.save()
        students[fields["surname"]] = student

    return students


# ------------------------------------------------------------------------------
# Absences


def create_absence_restriction_time():
    if AbsenceTime.objects.exists():
        return
    restriction_time = time(hour=9, minute=15)
    AbsenceTime.objects.create(absence_restriction_time=restriction_time)
    
    
def create_absences(students: dict[str, Student], nearest_day: datetime):
    date_f = "%Y-%m-%d"

    values = [
        {
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "student": students["Кацевалов"],
            "excuse": Absence.Excuse.LEGITIMATE.value,
            "reason": "Заболел",
            "status": Absence.Status.CLOSED.value,
            "comment": "Болеть будет недолго"
        },
        {
            "date": nearest_day.strftime(date_f),
            "student": students["Хромов"],
            "excuse": Absence.Excuse.LATE.value,
            "reason": "Электричка опоздала",
            "status": Absence.Status.CLOSED.value,
            "comment": ""
        },
        {
            "date": (nearest_day - timedelta(14)).strftime(date_f),
            "student": students["Хромов"],
            "excuse": Absence.Excuse.ILLEGITIMATE.value,
            "reason": "Прогул",
            "status": Absence.Status.OPEN,
            "comment": "Лежал дома на диване"
        },
    ]

    for value in values:
        absence, _ = Absence.objects.get_or_create(**value)
        absence.save()


# ------------------------------------------------------------------------------
# Punishments

def create_punishments(
    students: dict[str, Student],
    teachers: dict[str, Teacher], 
    nearest_day: datetime,
):
    date_f = "%Y-%m-%d"
    values = [
        {
            "student": students["Хромов"],
            "reason": "Не пришел на пары",
            "type": Punishment.Type.PUNISHMENT.value,
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "teacher": teachers["Никандров"],
            "remove_date": nearest_day.strftime(date_f),
        },
        {
            "student": students["Исаков"],
            "reason": "Сломал парту",
            "type": Punishment.Type.REBUKE.value,
            "date": nearest_day.strftime(date_f),
            "teacher": teachers["Репалов"],
            "remove_date": None,
        },
    ]

    for value in values:
        punishment, _ = Punishment.objects.get_or_create(**value)
        punishment.save()


# ------------------------------------------------------------------------------
# Encouragements

def create_encouragements(
    students: dict[str, Student],
    teachers: dict[str, Teacher],
    nearest_day: datetime,
):
    date_f = "%Y-%m-%d"
    values = [
        {
            "student": students["Хромов"],
            "reason": "За спортивные достижения",
            "type": Encouragement.Type.ENCOURAGEMENT.value,
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "teacher": teachers["Никандров"],
        },
        {
            "student": students["Исаков"],
            "reason": "За выступление на празднике",
            "type": Encouragement.Type.REMOVE_PUNISHMENT.value,
            "date": nearest_day.strftime(date_f),
            "teacher": teachers["Репалов"],
        },
    ]

    for value in values:
        encouragement, _ = Encouragement.objects.get_or_create(**value)
        encouragement.save()


# ------------------------------------------------------------------------------
# Achievements

def create_achievement_types():
    values = ["Спортивные", "Научные"]

    types = {}

    for value in values:
        type_, _ = AchievementType.objects.get_or_create(title=value)
        type_.save()
        types[value] = type_

    return types


def create_achievements(
    achievement_types: dict[str, AchievementType],
    students: dict[str, Student],
    nearest_day: datetime,
):
    date_f = "%Y-%m-%d"
    values = [
        {
            "student": students["Исаков"],
            "text": "Мастер спорта по футболу",
            "type": achievement_types["Спортивные"],
        },
        {
            "student": students["Хромов"],
            "text": "Написал научную статью",
            "type": achievement_types["Научные"],
            "date": nearest_day.strftime(date_f),
        },
    ]

    for value in values:
        achievement, _ = Achievement.objects.get_or_create(**value)
        achievement.save()


def create_subjects():
    """Not really create, just read from database."""

    values = [
        "Тактическая подготовка",
        "Тактико-специальная подготовка",
        "Военно-специальная подготовка",
        "Военно-инженерная подготовка",
        "Военно-политическая подготовка",
        "Военная топография",
        "Строевая подготовка",
    ]

    subjects = {}

    for value in values:
        subject = Subject.objects.get(title=value)
        subjects[value] = subject

    return subjects

# ------------------------------------------------------------------------------
# Lessons


def create_rooms():
    values = ["510", "Плац", "501", "502", "503", "504"]

    rooms = {}

    for value in values:
        room, _ = Room.objects.get_or_create(title=value)
        room.save()
        rooms[value] = room

    return rooms


def create_lessons(
    rooms: dict[str, Room],
    milgroups: dict[str, Milgroup],
    subjects: dict[str, Subject],
    nearest_day: datetime,
):
    date_f = "%Y-%m-%d"
    values = [
        {
            "type": Lesson.Type.LECTURE.value,
            "room": rooms["510"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 1,
            "subject": subjects["Тактическая подготовка"],
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "room": rooms["Плац"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 2,
            "subject": subjects["Строевая подготовка"],
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "room": rooms["504"],
            "milgroup": milgroups["1809"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 3,
            "subject": subjects["Военная топография"],
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "room": rooms["Плац"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 1,
            "subject": subjects["Строевая подготовка"],
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "room": rooms["504"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 2,
            "subject": subjects["Военная топография"],
        },
        {
            "type": Lesson.Type.LECTURE.value,
            "room": rooms["510"],
            "milgroup": milgroups["1810"],
            "date": nearest_day.strftime(date_f),
            "ordinal": 3,
            "subject": subjects["Тактическая подготовка"],
        },
        {
            "type": Lesson.Type.LECTURE.value,
            "room": rooms["510"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 1,
            "subject": subjects["Тактическая подготовка"],
        },
        {
            "type": Lesson.Type.PRACTICE.value,
            "room": rooms["Плац"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 2,
            "subject": subjects["Строевая подготовка"],
        },
        {
            "type": Lesson.Type.SEMINAR.value,
            "room": rooms["504"],
            "milgroup": milgroups["1809"],
            "date": (nearest_day - timedelta(7)).strftime(date_f),
            "ordinal": 3,
            "subject": subjects["Военная топография"],
        },
    ]

    lessons = []

    for value in values:
        lesson, _ = Lesson.objects.get_or_create(**value)
        lesson.save()
        lessons.append(lesson)

    return lessons

# ------------------------------------------------------------------------------
# Marks


def create_marks(lessons: list[Lesson], students: dict[str, Student]):
    values = [
        {
            "lesson": lessons[0],
            "student": students["Хромов"],
            "values": [5],
        },
        {
            "lesson": lessons[0],
            "student": students["Исаков"],
            "values": [4],
        },
        {
            "lesson": lessons[0],
            "student": students["Кацевалов"],
            "values": [3],
        },
        {
            "lesson": lessons[1],
            "student": students["Хромов"],
            "values": [5],
        },
        {
            "lesson": lessons[1],
            "student": students["Исаков"],
            "values": [3],
        },
        {
            "lesson": lessons[1],
            "student": students["Кацевалов"],
            "values": [2],
        },
    ]

    for value in values:
        mark, _ = Mark.objects.get_or_create(**value)
        mark.save()


# ------------------------------------------------------------------------------
# Uniforms


def create_uniforms(milfaculties: dict[str, Milfaculty]):
    for milfaculty in milfaculties.keys():
        value = {
            "headdress": "CA",
            "outerwear": "JA",
            "milfaculty": milfaculties[milfaculty],
        }
        uniform, _ = Uniform.objects.get_or_create(**value)
        uniform.save()
