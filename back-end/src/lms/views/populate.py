from datetime import (
    datetime,
    timedelta,
    time,
)

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

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
)
from lms.models.teachers import (
    Rank,
    TeacherPost,
    Teacher,
)
from lms.models.absences import (
    Absence,
    AbsenceTime,
)
from lms.models.encouragements import (
    Encouragement,)
from lms.models.punishments import (
    Punishment,)
from lms.models.achievements import (
    AchievementType,
    Achievement,
)
from lms.models.lessons import (
    Room,
    Lesson,
)
from lms.models.marks import Mark
from lms.functions import get_date_range

from common.models.subjects import Subject


def create_faculties():
    values = ['МИЭМ', 'МИЭФ', 'ФКН']

    faculties = {}

    for value in values:
        faculty, _ = Faculty.objects.get_or_create(faculty=value)
        faculty.save()
        faculties[value] = faculty

    return faculties


def create_milfaculties() -> dict[str, Milfaculty]:
    values = ['ВКС', 'Сержанты', 'Разведка', 'РВСН']

    milfaculties = {}

    for value in values:
        milfaculty, _ = Milfaculty.objects.get_or_create(milfaculty=value)
        milfaculty.save()
        milfaculties[value] = milfaculty

    return milfaculties


def create_programs(faculties: dict[str, Faculty]) -> dict[str, Program]:
    values = [{
        'code': '09.03.01',
        'program': 'Информатика и вычислительная техника',
        'faculty': faculties['МИЭМ']
    }, {
        'code': '09.03.04',
        'program': 'Программная инженерия',
        'faculty': faculties['ФКН']
    }, {
        'code': '15.03.01',
        'program': 'Машиностроение',
        'faculty': faculties['МИЭМ']
    }, {
        'code': '45.03.04',
        'program': 'Интеллектуальные системы в гуманитарной сфере',
        'faculty': faculties['МИЭМ']
    }]

    programs = {}

    for value in values:
        program, _ = Program.objects.get_or_create(
            code=value['code'],
            program=value['program'],
            faculty=value['faculty'],
        )
        program.save()
        programs[value['program']] = program

    return programs


def create_milgroups(
        milfaculties: dict[str, Milfaculty]) -> dict[int, Milgroup]:
    values = [{
        'milgroup': 1801,
        'weekday': 4,
        'milfaculty': milfaculties['Разведка']
    }, {
        'milgroup': 1802,
        'weekday': 4,
        'milfaculty': milfaculties['Разведка']
    }, {
        'milgroup': 1803,
        'weekday': 4,
        'milfaculty': milfaculties['Разведка']
    }, {
        'milgroup': 1804,
        'weekday': 4,
        'milfaculty': milfaculties['Сержанты']
    }, {
        'milgroup': 1805,
        'weekday': 4,
        'milfaculty': milfaculties['Сержанты']
    }, {
        'milgroup': 1806,
        'weekday': 4,
        'milfaculty': milfaculties['Сержанты']
    }, {
        'milgroup': 1807,
        'weekday': 4,
        'milfaculty': milfaculties['ВКС']
    }, {
        'milgroup': 1808,
        'weekday': 4,
        'milfaculty': milfaculties['ВКС']
    }, {
        'milgroup': 1809,
        'weekday': 4,
        'milfaculty': milfaculties['ВКС']
    }, {
        'milgroup': 1810,
        'weekday': 4,
        'milfaculty': milfaculties['РВСН']
    }, {
        'milgroup': 1811,
        'weekday': 4,
        'milfaculty': milfaculties['РВСН']
    }, {
        'milgroup': 1812,
        'weekday': 4,
        'milfaculty': milfaculties['РВСН']
    }]

    milgroups = {}

    for value in values:
        milgroup, _ = Milgroup.objects.get_or_create(
            milgroup=value['milgroup'],
            milfaculty=value['milfaculty'],
            weekday=value['weekday'],
        )
        milgroup.save()
        milgroups[value['milgroup']] = milgroup

    return milgroups


def create_ranks() -> dict[str, Rank]:
    values = ['Подполковник', 'Полковник', 'Майор', 'Генерал-майор']

    ranks = {}

    for value in values:
        rank, _ = Rank.objects.get_or_create(rank=value)
        rank.save()
        ranks[value] = rank

    return ranks


def create_posts() -> dict[str, TeacherPost]:
    values = ['Начальник цикла', 'Преподаватель', 'Профессор', 'Начальник ВУЦ']

    posts = {}

    for value in values:
        post, _ = TeacherPost.objects.get_or_create(teacher_post=value)
        post.save()
        posts[value] = post

    return posts


def create_passports() -> dict[str, Passport]:
    values = [{
        'series': '0000',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '1111',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '2222',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '3333',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '4444',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '5555',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }, {
        'series': '6666',
        'code': '111111',
        'ufms_name': 'УФМС гор. Москвы',
        'ufms_code': '740-056',
        'issue_date': '2020-10-02',
    }]

    passports = {}

    for fields in values:
        passport, _ = Passport.objects.get_or_create(**fields)
        passports[fields['series']] = passport

    return passports


def create_recruitments_offices() -> dict[str, RecruitmentOffice]:
    values = [{
        'city': 'Москва',
        'district': 'Центрального',
    }]

    offices = {}

    for fields in values:
        office, _ = RecruitmentOffice.objects.get_or_create(**fields)
        offices[fields['city']] = office

    return offices


def create_university_infos() -> dict[str, UniversityInfo]:
    values = [{
        'id_card': 'HSE11229',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE1129',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE11319',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE1889',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE11255',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE1199',
        'group_title': 'БИТ 188',
    }, {
        'id_card': 'HSE7779',
        'group_title': 'БИТ 188',
    }]

    infos = {}

    for fields in values:
        info, _ = UniversityInfo.objects.get_or_create(**fields)
        infos[fields['id_card']] = info

    return infos


# pylint: disable=(too-many-locals)
def create_students(
    milgroups: dict[int, Milgroup],
    programs: dict[str, Program],
    milspecialties: dict[str, Milspecialty],
    passports: dict[str, Passport],
    recruitment_offices: dict[str, RecruitmentOffice],
    university_infos: dict[str, UniversityInfo],
):
    # pylint: disable=too-many-arguments

    # TODO – index term
    # FIXME(TmLev): provide family for every student

    values = [{
        'surname': 'Хромов',
        'name': 'Григорий',
        'patronymic': 'Александрович',
        'milgroup': milgroups[1809],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '2000-11-04',
        'program': programs['Информатика и вычислительная техника'],
        'status': Student.Status.STUDENT.value,
        'photo': None,
        'surname_genitive': 'Хромова',
        'name_genitive': 'Григория',
        'patronymic_genitive': 'Александровича',
        'passport': passports['0000'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE11229']
    }, {
        'surname': 'Кацевалов',
        'name': 'Артем',
        'patronymic': 'Сергеевич',
        'milgroup': milgroups[1809],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '2000-02-23',
        'program': programs['Информатика и вычислительная техника'],
        'status': Student.Status.STUDENT.value,
        'photo': None,
        'surname_genitive': 'Кацевалова',
        'name_genitive': 'Артема',
        'patronymic_genitive': 'Сергеевича',
        'passport': passports['1111'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE1129'],
    }, {
        'surname': 'Исаков',
        'name': 'Владислав',
        'patronymic': 'Евгеньевич',
        'milgroup': milgroups[1809],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '1999-08-29',
        'program': programs['Информатика и вычислительная техника'],
        'status': Student.Status.STUDENT.value,
        'photo': None,
        'surname_genitive': 'Исакова',
        'name_genitive': 'Владислава',
        'patronymic_genitive': 'Евгеньевича',
        'passport': passports['2222'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE11319'],
    }, {
        'surname': 'Алиев',
        'name': 'Насир',
        'patronymic': 'Ашурович',
        'milgroup': milgroups[1808],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '1999-05-14',
        'program': programs['Информатика и вычислительная техника'],
        'status': Student.Status.STUDENT.value,
        'photo': None,
        'surname_genitive': 'Алиева',
        'name_genitive': 'Насира',
        'patronymic_genitive': 'Ашуровича',
        'passport': passports['3333'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE1889'],
    }, {
        'surname': 'Куркин',
        'name': 'Андрей',
        'patronymic': 'Витальевич',
        'milgroup': milgroups[1812],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '1999-11-12',
        'program': programs['Информатика и вычислительная техника'],
        'status': Student.Status.STUDENT.value,
        'photo': None,
        'surname_genitive': 'Куркина',
        'name_genitive': 'Андрея',
        'patronymic_genitive': 'Витальевича',
        'passport': passports['4444'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE11255'],
    }, {
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': 'Сидорович',
        'milgroup': milgroups[1804],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '1999-05-04',
        'program': programs['Машиностроение'],
        'status': Student.Status.DEDUCTED.value,
        'photo': None,
        'surname_genitive': 'Иванова',
        'name_genitive': 'Петра',
        'patronymic_genitive': 'Сидоровича',
        'passport': passports['5555'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE1199'],
    }, {
        'surname': 'Чукмарикадзе',
        'name': 'Губарибек',
        'patronymic': 'Алкинбеков',
        'milgroup': milgroups[1801],
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'birthdate': '1969-04-13',
        'program': programs['Интеллектуальные системы в гуманитарной сфере'],
        'status': Student.Status.GRADUATED.value,
        'photo': None,
        'surname_genitive': 'Чукмаридзе',
        'name_genitive': 'Губарибека',
        'patronymic_genitive': 'Алкинбекова',
        'passport': passports['6666'],
        'recruitment_office': recruitment_offices['Москва'],
        'university_info': university_infos['HSE7779'],
    }]

    students = {}

    for fields in values:
        student, _ = Student.objects.get_or_create(**fields)
        student.save()
        students[fields['surname']] = student

    return students


# pylint: disable=(too-many-locals)
def create_absences(students: dict[str, Student], nearest_day: datetime):
    date_f = '%Y-%m-%d'

    values = [
        {
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'student': students['Кацевалов'],
            'type': Absence.Type.SERIOUS.value,
            'reason': 'Заболел',
            'status': Absence.Status.CLOSED.value,
            'comment': 'Болеть будет недолго'
        },
        {
            'date': nearest_day.strftime(date_f),
            'student': students['Хромов'],
            'type': Absence.Type.LATE.value,
            'reason': 'Электричка опоздала',
            'status': Absence.Status.CLOSED.value,
            'comment': ''
        },
        {
            'date': (nearest_day - timedelta(14)).strftime(date_f),
            'student': students['Хромов'],
            'type': Absence.Type.NOT_SERIOUS.value,
            'reason': 'Прогул',
            'status': Absence.Status.OPEN,
            'comment': 'Лежал дома на диване'
        },
    ]

    for value in values:
        absence, _ = Absence.objects.get_or_create(date=value['date'],
                                                   student=value['student'],
                                                   type=value['type'],
                                                   reason=value['reason'],
                                                   status=value['status'],
                                                   comment=value['comment'])
        absence.save()


# pylint: disable=(too-many-locals)
# pylint: disable=(too-many-arguments)
def create_teachers(
    milgroups: dict[int, Milgroup],
    milfaculties: dict[str, Milfaculty],
    ranks: dict[str, Rank],
    posts: dict[str, TeacherPost],
):
    values = [
        {
            'surname': 'Никандров',
            'name': 'Игорь',
            'patronymic': 'Владимирович',
            'milfaculty': milfaculties['ВКС'],
            'rank': ranks['Подполковник'],
            'teacher_post': posts['Преподаватель'],
            'milgroup': milgroups[1809]
        },
        {
            'surname': 'Репалов',
            'name': 'Дмитрий',
            'patronymic': 'Николаевич',
            'milfaculty': milfaculties['ВКС'],
            'rank': ranks['Подполковник'],
            'teacher_post': posts['Начальник цикла'],
            'milgroup': milgroups[1808]
        },
        {
            'surname': 'Мещеряков',
            'name': 'Иван',
            'patronymic': 'Владимирович',
            'milfaculty': milfaculties['Сержанты'],
            'rank': ranks['Майор'],
            'teacher_post': posts['Преподаватель'],
            'milgroup': milgroups[1806]
        },
        {
            'surname': 'Ковальчук',
            'name': 'Игорь',
            'patronymic': 'Валентинович',
            'milfaculty': milfaculties['Разведка'],
            'rank': ranks['Полковник'],
            'teacher_post': posts['Начальник цикла'],
            'milgroup': milgroups[1801]
        },
        {
            'surname': 'Гаврилов',
            'name': 'Климент',
            'patronymic': 'Сергеевич',
            'milfaculty': milfaculties['РВСН'],
            'rank': ranks['Генерал-майор'],
            'teacher_post': posts['Преподаватель'],
            'milgroup': None
        },
    ]

    teachers = {}

    for value in values:
        teacher, _ = Teacher.objects.get_or_create(
            surname=value['surname'],
            name=value['name'],
            patronymic=value['patronymic'],
            milfaculty=value['milfaculty'],
            rank=value['rank'],
            teacher_post=value['teacher_post'],
            milgroup=value['milgroup'],
        )
        teacher.save()
        teachers[value['surname']] = teacher
    return teachers


def create_punishments(students: dict[str, Student],
                       teachers: dict[str, Teacher], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'student': students['Хромов'],
            'reason': 'Не пришел на пары',
            'type': Punishment.Type.PUNISHMENT.value,
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher': teachers['Никандров'],
            'remove_date': nearest_day.strftime(date_f),
        },
        {
            'student': students['Исаков'],
            'reason': 'Сломал парту',
            'type': Punishment.Type.REBUKE.value,
            'date': nearest_day.strftime(date_f),
            'teacher': teachers['Репалов'],
            'remove_date': None,
        },
    ]

    for value in values:
        punishment, _ = Punishment.objects.get_or_create(**value)
        punishment.save()


def create_encouragements(students: dict[str, Student],
                          teachers: dict[str, Teacher], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'student': students['Хромов'],
            'reason': 'За спортивные достижения',
            'type': Encouragement.Type.ENCOURAGEMENT.value,
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher': teachers['Никандров'],
        },
        {
            'student': students['Исаков'],
            'reason': 'За выступление на празднике',
            'type': Encouragement.Type.REMOVE_PUNISHMENT.value,
            'date': nearest_day.strftime(date_f),
            'teacher': teachers['Репалов'],
        },
    ]

    for value in values:
        encouragement, _ = Encouragement.objects.get_or_create(**value)
        encouragement.save()


def create_achievement_types():
    values = ['Спортивные', 'Научные']

    types = {}

    for value in values:
        type_, _ = AchievementType.objects.get_or_create(achievement_type=value)
        type_.save()
        types[value] = type_

    return types


def create_mil_specialty():
    values = [{
        'code': '094001',
        'mil_specialty': 'Применение наземных подразделений войсковой разведки',
    }, {
        'code': '411300',
        'mil_specialty': 'Эксплуатация и ремонт автоматизированных систем '
                         'комплексов баллистических стратегических ракет '
                         'наземного базирования',
    }, {
        'code': '453000',
        'mil_specialty':
            'Организация эксплуатации и ремонта автоматизированных '
            'систем управления и вычислительных комплексов '
            'ракетно-космической обороны',
    }, {
        'code': '453100',
        'mil_specialty':
            'Математическое и программное обеспечение функционирования '
            'вычислительных комплексов ракетно-космической обороны',
    }, {
        'code': '751100',
        'mil_specialty': 'Защита информационных технологий',
    }, {
        'code': '100182',
        'mil_specialty': 'Стрелковые, командир стрелкового отделения',
    }, {
        'code': '106646-543',
        'mil_specialty': 'Разведывательные, разведчик-оператор СБР, ПСНР',
    }]

    specs = {}

    for value in values:
        spec, _ = Milspecialty.objects.get_or_create(
            mil_specialty=value['mil_specialty'],
            code=value['code'],
        )
        spec.save()
        specs[value['mil_specialty']] = spec

    return specs


def create_achievements(
    achievement_types: dict[str, AchievementType],
    students: dict[str, Student],
    nearest_day: datetime,
):
    date_f = '%Y-%m-%d'
    values = [
        {
            'student': students['Исаков'],
            'text': 'Мастер спорта по футболу',
            'achievement_type': achievement_types['Спортивные'],
        },
        {
            'student': students['Хромов'],
            'text': 'Написал научную статью',
            'achievement_type': achievement_types['Научные'],
            'date': nearest_day.strftime(date_f),
        },
    ]

    for value in values:
        achievement, _ = Achievement.objects.get_or_create(**value)
        achievement.save()


def create_rooms():
    values = ['510', 'Плац', '501', '502', '503', '504']

    rooms = {}

    for value in values:
        room, _ = Room.objects.get_or_create(room=value)
        room.save()
        rooms[value] = room

    return rooms


def create_subjects():
    """Not really create, just read from database."""

    values = [
        'Тактическая подготовка',
        'Тактико-специальная подготовка',
        'Военно-специальная подготовка',
        'Военно-инженерная подготовка',
        'Военно-политическая подготовка',
        'Военная топография',
        'Строевая подготовка',
    ]

    subjects = {}

    for value in values:
        subject = Subject.objects.get(title=value)
        subjects[value] = subject

    return subjects


def create_lessons(rooms: dict[str, Room], milgroups: dict[int, Milgroup],
                   subjects: dict[str, Subject], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'lesson_type': Lesson.LessonType.LECTURE.value,
            'room': rooms['510'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.PRACTICE.value,
            'room': rooms['Плац'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.SEMINAR.value,
            'room': rooms['504'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 3,
            'subject': subjects['Военная топография'],
        },
        {
            'lesson_type': Lesson.LessonType.PRACTICE.value,
            'room': rooms['Плац'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.SEMINAR.value,
            'room': rooms['504'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Военная топография'],
        },
        {
            'lesson_type': Lesson.LessonType.LECTURE.value,
            'room': rooms['510'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 3,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.LECTURE.value,
            'room': rooms['510'],
            'milgroup': milgroups[1809],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.PRACTICE.value,
            'room': rooms['Плац'],
            'milgroup': milgroups[1809],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': Lesson.LessonType.SEMINAR.value,
            'room': rooms['504'],
            'milgroup': milgroups[1809],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'ordinal': 3,
            'subject': subjects['Военная топография'],
        },
    ]

    lessons = []

    for value in values:
        lesson, _ = Lesson.objects.get_or_create(**value)
        lesson.save()
        lessons.append(lesson)

    return lessons


def create_marks(lessons: list[Lesson], students: dict[str, Student]):
    values = [
        {
            'lesson': lessons[0],
            'student': students['Хромов'],
            'mark': [5],
        },
        {
            'lesson': lessons[0],
            'student': students['Исаков'],
            'mark': [4],
        },
        {
            'lesson': lessons[0],
            'student': students['Кацевалов'],
            'mark': [3],
        },
        {
            'lesson': lessons[1],
            'student': students['Хромов'],
            'mark': [5],
        },
        {
            'lesson': lessons[1],
            'student': students['Исаков'],
            'mark': [3],
        },
        {
            'lesson': lessons[1],
            'student': students['Кацевалов'],
            'mark': [2],
        },
    ]

    for value in values:
        mark, _ = Mark.objects.get_or_create(**value)
        mark.save()


def create_absence_restriction_time():
    restriction_time = time(hour=9, minute=15)
    AbsenceTime.objects.create(absence_restriction_time=restriction_time)


# pylint: disable=(too-many-locals)
@api_view(['POST'])
@permission_classes((AllowAny,))
def lms_populate(request: Request) -> Response:
    """
    Populate database with fake students, users, etc. (including super user).
    :param request: empty PUT request.
    :return: response indicating whether request was successful (probably was).
    """

    faculties = create_faculties()
    programs = create_programs(faculties)
    milfaculties = create_milfaculties()
    milgroups = create_milgroups(milfaculties)
    ranks = create_ranks()
    posts = create_posts()
    milspecialties = create_mil_specialty()

    # nearest day for 18XX milgroups
    nearest_day = datetime.strptime(
        get_date_range(datetime.now() - timedelta(6), datetime.now(), 4)[0],
        '%Y-%m-%d')

    passports = create_passports()
    offices = create_recruitments_offices()
    infos = create_university_infos()
    students = create_students(
        milgroups,
        programs,
        milspecialties,
        passports,
        offices,
        infos,
    )

    teachers = create_teachers(milgroups, milfaculties, ranks, posts)

    create_absences(students, nearest_day)

    create_punishments(students, teachers, nearest_day)

    create_encouragements(students, teachers, nearest_day)

    achievement_types = create_achievement_types()
    create_achievements(achievement_types, students, nearest_day)

    subjects = create_subjects()
    rooms = create_rooms()
    lessons = create_lessons(rooms, milgroups, subjects, nearest_day)

    create_absence_restriction_time()

    create_marks(lessons, students)
    return Response({'message': 'Population successful'},
                    status=HTTP_201_CREATED)
