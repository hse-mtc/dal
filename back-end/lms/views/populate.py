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
)
from lms.models.students import (
    Status,
    Program,
    Student,
    MilSpecialty,
    Faculty,
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
    Encouragement,
)
from lms.models.punishments import (
    Punishment,
)
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


def create_statuses() -> dict[str, Status]:
    values = ['Завершил', 'Обучается', 'Отчислен']

    statuses = {}

    for value in values:
        status, _ = Status.objects.get_or_create(status=value)
        status.save()
        statuses[value] = status

    return statuses


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


# pylint: disable=(too-many-locals)
def create_students(
    milgroups: dict[int, Milgroup],
    programs: dict[str, Program],
    statuses: dict[str, Status],
    milspecialties: dict[str, MilSpecialty],
):
    values = [{
        'surname': 'Хромов',
        'name': 'Григорий',
        'patronymic': 'Александрович',
        'milgroup': milgroups[1809],
        'birthdate': '2000-11-04',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None,
        'surname_genitive': 'Хромова',
        'name_genitive': 'Григория',
        'patronymic_genitive': 'Александровича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE11229',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Кацевалов',
        'name': 'Артем',
        'patronymic': 'Сергеевич',
        'milgroup': milgroups[1809],
        'birthdate': '2000-02-23',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None,
        'surname_genitive': 'Кацевалова',
        'name_genitive': 'Артема',
        'patronymic_genitive': 'Сергеевича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE11239',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Исаков',
        'name': 'Владислав',
        'patronymic': 'Евгеньевич',
        'milgroup': milgroups[1809],
        'birthdate': '1999-08-29',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None,
        'surname_genitive': 'Исакова',
        'name_genitive': 'Владислава',
        'patronymic_genitive': 'Евгеньевича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE11219',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Алиев',
        'name': 'Насир',
        'patronymic': 'Ашурович',
        'milgroup': milgroups[1808],
        'birthdate': '1999-05-14',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None,
        'surname_genitive': 'Алиева',
        'name_genitive': 'Насира',
        'patronymic_genitive': 'Ашуровича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE1889',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Куркин',
        'name': 'Андрей',
        'patronymic': 'Витальевич',
        'milgroup': milgroups[1812],
        'birthdate': '1999-11-12',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None,
        'surname_genitive': 'Куркина',
        'name_genitive': 'Андрея',
        'patronymic_genitive': 'Витальевича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE11255',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': 'Сидорович',
        'milgroup': milgroups[1804],
        'birthdate': '1999-05-04',
        'program': programs['Машиностроение'],
        'status': statuses['Отчислен'],
        'photo': None,
        'surname_genitive': 'Иванова',
        'name_genitive': 'Петра',
        'patronymic_genitive': 'Сидоровича',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE1199',
        'hse_group': 'БИТ 188'
    }, {
        'surname': 'Чукмарикадзе',
        'name': 'Губарибек',
        'patronymic': 'Алкинбеков',
        'milgroup': milgroups[1801],
        'birthdate': '1969-04-13',
        'program': programs['Интеллектуальные системы в гуманитарной сфере'],
        'status': statuses['Завершил'],
        'photo': None,
        'surname_genitive': 'Чукмаридзе',
        'name_genitive': 'Губарибека',
        'patronymic_genitive': 'Алкинбекова',
        'passport_series': '1111',
        'passport_code': '111111',
        'passport_ufms_name': 'УФМС гор. Москвы',
        'passport_ufms_code': '740-056',
        'passport_date': '2020-10-02',
        'commissariat_city': 'г. Москва',
        'commissariat_district': 'Центрального',
        'mil_specialty': milspecialties['Защита информационных технологий'],
        'hse_id': 'HSE7779',
        'hse_group': 'БИТ 188'
    }]

    students = {}

    for value in values:
        student, _ = Student.objects.get_or_create(
            surname=value['surname'],
            name=value['name'],
            patronymic=value['patronymic'],
            milgroup=value['milgroup'],
            birthdate=value['birthdate'],
            program=value['program'],
            status=value['status'],
            photo=value['photo'],
            surname_genitive=value['surname_genitive'],
            name_genitive=value['name_genitive'],
            patronymic_genitive=value['patronymic_genitive'],
            passport_series=value['passport_series'],
            passport_code=value['passport_code'],
            passport_ufms_name=value['passport_ufms_name'],
            passport_ufms_code=value['passport_ufms_code'],
            passport_date=value['passport_date'],
            commissariat_city=value['commissariat_city'],
            commissariat_district=value['commissariat_district'],
            mil_specialty=value['mil_specialty'],
            hse_id=value['hse_id'],
            hse_group=value['hse_group'],
        )
        student.save()
        students[value['surname']] = student

    return students


# pylint: disable=(too-many-locals)
def create_absences(students: dict[str, Student], nearest_day: datetime):
    date_f = '%Y-%m-%d'

    values = [
        {
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'student': students['Кацевалов'],
            'absence_type': Absence.AbsenceType.SERIOUS.value,
            'reason': 'Заболел',
            'absence_status': Absence.AbsenceStatus.CLOSED.value,
            'comment': 'Болеть будет недолго'
        },
        {
            'date': nearest_day.strftime(date_f),
            'student': students['Хромов'],
            'absence_type': Absence.AbsenceType.LATE.value,
            'reason': 'Электричка опоздала',
            'absence_status': Absence.AbsenceStatus.CLOSED.value,
            'comment': ''
        },
        {
            'date': (nearest_day - timedelta(14)).strftime(date_f),
            'student': students['Хромов'],
            'absence_type': Absence.AbsenceType.NOT_SERIOUS.value,
            'reason': 'Прогул',
            'absence_status': Absence.AbsenceStatus.OPEN,
            'comment': 'Лежал дома на диване'
        },
    ]

    for value in values:
        absence, _ = Absence.objects.get_or_create(
            date=value['date'],
            student=value['student'],
            absence_type=value['absence_type'],
            reason=value['reason'],
            absence_status=value['absence_status'],
            comment=value['comment'],
        )
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
            'punishment_type': Punishment.PunishmentType.PUNISHMENT.value,
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher': teachers['Никандров'],
            'remove_date': nearest_day.strftime(date_f),
        },
        {
            'student': students['Исаков'],
            'reason': 'Сломал парту',
            'punishment_type': Punishment.PunishmentType.REBUKE.value,
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
            'student':
                students['Хромов'],
            'reason':
                'За спортивные достижения',
            'encouragement_type':
                Encouragement.EncouragementType.ENCOURAGEMENT.value,
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher':
                teachers['Никандров'],
        },
        {
            'student':
                students['Исаков'],
            'reason':
                'За выступление на празднике',
            'encouragement_type':
                Encouragement.EncouragementType.REMOVE_PUNISHMENT.value,
            'date':
                nearest_day.strftime(date_f),
            'teacher':
                teachers['Репалов'],
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
        spec, _ = MilSpecialty.objects.get_or_create(
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


def create_lessons(rooms: dict[str, Room], milgroups: dict[str, Milgroup],
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
    statuses = create_statuses()
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

    students = create_students(milgroups, programs, statuses, milspecialties)

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
