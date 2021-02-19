from datetime import datetime, timedelta, time

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from lms.models.common import Milfaculty, Milgroup
from lms.models.student import Status, Program, Student
from lms.models.teacher import Rank, TeacherPost, Teacher
from lms.models.absence import (AbsenceStatus, AbsenceType, Absence,
                                AbsenceTime)
from lms.models.encouragement import EncouragementType, Encouragement
from lms.models.punishment import PunishmentType, Punishment
from lms.models.achievement import AchievementType, Achievement
from lms.models.lesson import Room, LessonType, Lesson
from lms.models.mark import Mark
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


def create_programs() -> dict[str, Program]:
    values = [{
        'code': '09.03.01',
        'program': 'Информатика и вычислительная техника'
    }, {
        'code': '09.03.04',
        'program': 'Программная инженерия'
    }, {
        'code': '15.03.01',
        'program': 'Машиностроение'
    }, {
        'code': '45.03.04',
        'program': 'Интеллектуальные системы в гуманитарной сфере'
    }]
    programs = {}

    for value in values:
        program, _ = Program.objects.get_or_create(code=value['code'],
                                                   program=value['program'])
        program.save()
        programs[value['program']] = program

    return programs


def create_milfaculties() -> dict[str, Milfaculty]:
    values = ['ВКС', 'Сержанты', 'Разведка', 'РВСН']
    milfaculties = {}

    for value in values:
        milfaculty, _ = Milfaculty.objects.get_or_create(milfaculty=value)
        milfaculty.save()
        milfaculties[value] = milfaculty

    return milfaculties


def create_milgroups(
        milfaculties: dict[str, Milfaculty]) -> dict[str, Milgroup]:
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
            weekday=value['weekday'])
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
def create_students(milgroups: dict[int, Milgroup],
                    programs: dict[str, Program], statuses: dict[str, Status]):
    values = [{
        'surname': 'Хромов',
        'name': 'Григорий',
        'patronymic': 'Александрович',
        'milgroup': milgroups[1809],
        'birthdate': '2000-11-04',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None
    }, {
        'surname': 'Кацевалов',
        'name': 'Артем',
        'patronymic': 'Сергеевич',
        'milgroup': milgroups[1809],
        'birthdate': '2000-02-23',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None
    }, {
        'surname': 'Исаков',
        'name': 'Владислав',
        'patronymic': 'Евгеньевич',
        'milgroup': milgroups[1809],
        'birthdate': '1999-08-29',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None
    }, {
        'surname': 'Алиев',
        'name': 'Насир',
        'patronymic': 'Ашурович',
        'milgroup': milgroups[1808],
        'birthdate': '1999-05-14',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None
    }, {
        'surname': 'Куркин',
        'name': 'Андрей',
        'patronymic': 'Витальевич',
        'milgroup': milgroups[1812],
        'birthdate': '1999-11-12',
        'program': programs['Информатика и вычислительная техника'],
        'status': statuses['Обучается'],
        'photo': None
    }, {
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': 'Сидорович',
        'milgroup': milgroups[1804],
        'birthdate': '1999-05-04',
        'program': programs['Машиностроение'],
        'status': statuses['Отчислен'],
        'photo': None
    }, {
        'surname': 'Чукмарикадзе',
        'name': 'Губарибек',
        'patronymic': 'Алкинбеков',
        'milgroup': milgroups[1801],
        'birthdate': '1969-04-13',
        'program': programs['Интеллектуальные системы в гуманитарной сфере'],
        'status': statuses['Завершил'],
        'photo': None
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
            photo=value['photo'])
        student.save()
        students[value['surname']] = student
    return students


def create_absence_types():
    values = ['Уважительная', 'Опоздание', 'Неуважительная']

    types = {}
    for value in values:
        typ, _ = AbsenceType.objects.get_or_create(absence_type=value)
        typ.save()
        types[value] = typ
    return types


def create_absence_statuses():
    values = ['Открыт', 'Закрыт']

    types = {}
    for value in values:
        typ, _ = AbsenceStatus.objects.get_or_create(absence_status=value)
        typ.save()
        types[value] = typ
    return types


# pylint: disable=(too-many-locals)
def create_absences(types: dict[str, AbsenceType],
                    statuses: dict[str, AbsenceStatus],
                    students: dict[str, Student], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'student': students['Кацевалов'],
            'absence_type': types['Уважительная'],
            'reason': 'Заболел',
            'absence_status': statuses['Закрыт'],
            'comment': 'Болеть будет недолго'
        },
        {
            'date': nearest_day.strftime(date_f),
            'student': students['Хромов'],
            'absence_type': types['Опоздание'],
            'reason': 'Электричка опоздала',
            'absence_status': statuses['Закрыт'],
            'comment': ''
        },
        {
            'date': (nearest_day - timedelta(14)).strftime(date_f),
            'student': students['Хромов'],
            'absence_type': types['Неуважительная'],
            'reason': 'Прогул',
            'absence_status': statuses['Открыт'],
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
            comment=value['comment'])
        absence.save()


# pylint: disable=(too-many-locals)
# pylint: disable=(too-many-arguments)
def create_teachers(milgroups: dict[int, Milgroup],
                    milfaculties: dict[str, Milfaculty], ranks: dict[str, Rank],
                    posts: dict[str, TeacherPost]):
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
            milgroup=value['milgroup'])
        teacher.save()
        teachers[value['surname']] = teacher
    return teachers


def create_punishment_types():
    values = ['Взыскание', 'Выговор', 'Отчисление']

    types = {}
    for value in values:
        typ, _ = PunishmentType.objects.get_or_create(punishment_type=value)
        typ.save()
        types[value] = typ
    return types


def create_punishments(punishment_types: dict[str, PunishmentType],
                       students: dict[str, Student],
                       teachers: dict[str, Teacher], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'student': students['Хромов'],
            'reason': 'Не пришел на пары',
            'punishment_type': punishment_types['Взыскание'],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher': teachers['Никандров'],
            'remove_date': nearest_day.strftime(date_f),
        },
        {
            'student': students['Исаков'],
            'reason': 'Сломал парту',
            'punishment_type': punishment_types['Выговор'],
            'date': nearest_day.strftime(date_f),
            'teacher': teachers['Репалов'],
            'remove_date': None,
        },
    ]

    for value in values:
        punishment, _ = Punishment.objects.get_or_create(**value)
        punishment.save()


def create_encouragement_types():
    values = ['Благодарность', 'Снятие взыскания']

    types = {}
    for value in values:
        typ, _ = EncouragementType.objects.get_or_create(
            encouragement_type=value)
        typ.save()
        types[value] = typ
    return types


def create_encouragements(encouragement_types: dict[str, EncouragementType],
                          students: dict[str, Student],
                          teachers: dict[str, Teacher], nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'student': students['Хромов'],
            'reason': 'За спортивные достижения',
            'encouragement_type': encouragement_types['Благодарность'],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'teacher': teachers['Никандров'],
        },
        {
            'student': students['Исаков'],
            'reason': 'За выступление на празднике',
            'encouragement_type': encouragement_types['Снятие взыскания'],
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
        typ, _ = AchievementType.objects.get_or_create(achievement_type=value)
        typ.save()
        types[value] = typ
    return types


def create_achievements(achievement_types: dict[str, AchievementType],
                        students: dict[str, Student], nearest_day: datetime):
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

    types = {}
    for value in values:
        typ, _ = Room.objects.get_or_create(room=value)
        typ.save()
        types[value] = typ
    return types


def create_lesson_types():
    values = ['Семинар', 'Лекция', 'Групповое занятие', 'Практическое занятие']

    types = {}
    for value in values:
        typ, _ = LessonType.objects.get_or_create(lesson_type=value)
        typ.save()
        types[value] = typ
    return types


def create_subjects():
    values = [
        'Тактическая подготовка',
        'Тактико-специальная подготовка',
        'Военно-специальная подготовка',
        'Военно-инженерная подготовка',
        'Военно-политическая подготовка',
        'Военная топография',
        'Строевая подготовка',
    ]

    types = {}
    for value in values:
        typ = Subject.objects.get(title=value)
        typ.save()
        types[value] = typ
    return types


def create_lessons(lesson_types: dict[str, LessonType], rooms: dict[str, Room],
                   milgroups: dict[str, Milgroup], subjects: dict[str, Subject],
                   nearest_day: datetime):
    date_f = '%Y-%m-%d'
    values = [
        {
            'lesson_type': lesson_types['Лекция'],
            'room': rooms['510'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': lesson_types['Практическое занятие'],
            'room': rooms['Плац'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': lesson_types['Семинар'],
            'room': rooms['504'],
            'milgroup': milgroups[1809],
            'date': nearest_day.strftime(date_f),
            'ordinal': 3,
            'subject': subjects['Военная топография'],
        },
        {
            'lesson_type': lesson_types['Практическое занятие'],
            'room': rooms['Плац'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': lesson_types['Семинар'],
            'room': rooms['504'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Военная топография'],
        },
        {
            'lesson_type': lesson_types['Лекция'],
            'room': rooms['510'],
            'milgroup': milgroups[1810],
            'date': nearest_day.strftime(date_f),
            'ordinal': 3,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': lesson_types['Лекция'],
            'room': rooms['510'],
            'milgroup': milgroups[1809],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'ordinal': 1,
            'subject': subjects['Тактическая подготовка'],
        },
        {
            'lesson_type': lesson_types['Практическое занятие'],
            'room': rooms['Плац'],
            'milgroup': milgroups[1809],
            'date': (nearest_day - timedelta(7)).strftime(date_f),
            'ordinal': 2,
            'subject': subjects['Строевая подготовка'],
        },
        {
            'lesson_type': lesson_types['Семинар'],
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

    statuses = create_statuses()
    programs = create_programs()
    milfaculties = create_milfaculties()
    milgroups = create_milgroups(milfaculties)
    ranks = create_ranks()
    posts = create_posts()

    # nearest day for 18XX milgroups
    nearest_day = datetime.strptime(
        get_date_range(datetime.now() - timedelta(6), datetime.now(), 4)[0],
        '%Y-%m-%d')

    students = create_students(milgroups, programs, statuses)

    teachers = create_teachers(milgroups, milfaculties, ranks, posts)

    absence_types = create_absence_types()
    absence_statuses = create_absence_statuses()

    create_absences(absence_types, absence_statuses, students, nearest_day)

    punishment_types = create_punishment_types()
    create_punishments(punishment_types, students, teachers, nearest_day)

    encouragement_types = create_encouragement_types()
    create_encouragements(encouragement_types, students, teachers, nearest_day)

    achievement_types = create_achievement_types()
    create_achievements(achievement_types, students, nearest_day)

    subjects = create_subjects()
    rooms = create_rooms()
    lesson_types = create_lesson_types()
    lessons = create_lessons(lesson_types, rooms, milgroups, subjects,
                             nearest_day)

    create_marks(lessons, students)
    create_absence_restriction_time()

    return Response({'message': 'Population successful'},
                    status=HTTP_201_CREATED)
