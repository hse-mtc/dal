import typing as tp

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from lms.models import (Status, Program, Milgroup, Milfaculty, Rank,
                        TeacherPost, Student, Teacher, AbsenceType,
                        AbsenceStatus, Absence, PunishmentType, Punishment)


def create_statuses() -> tp.Dict[str, Status]:
    values = ['Завершил', 'Обучается', 'Отчислен']
    statuses = {}

    for value in values:
        status, _ = Status.objects.get_or_create(status=value)
        status.save()
        statuses[value] = status

    return statuses


def create_programs() -> tp.Dict[str, Program]:
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


def create_milfaculties() -> tp.Dict[str, Milfaculty]:
    values = ['ВКС', 'Сержанты', 'Разведка', 'РВСН']
    milfaculties = {}

    for value in values:
        milfaculty, _ = Milfaculty.objects.get_or_create(milfaculty=value)
        milfaculty.save()
        milfaculties[value] = milfaculty

    return milfaculties


def create_milgroups(
        milfaculties: tp.Dict[str, Milfaculty]) -> tp.Dict[str, Milgroup]:
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


def create_ranks() -> tp.Dict[str, Rank]:
    values = ['Подполковник', 'Полковник', 'Майор', 'Генерал-майор']

    ranks = {}

    for value in values:
        rank, _ = Rank.objects.get_or_create(rank=value)
        rank.save()
        ranks[value] = rank

    return ranks


def create_posts() -> tp.Dict[str, TeacherPost]:
    values = ['Начальник цикла', 'Преподаватель', 'Профессор', 'Начальник ВУЦ']

    posts = {}

    for value in values:
        post, _ = TeacherPost.objects.get_or_create(teacher_post=value)
        post.save()
        posts[value] = post

    return posts


# pylint: disable=(too-many-locals)
def create_students(milgroups: tp.Dict[int, Milgroup],
                    programs: tp.Dict[str, Program], statuses: tp.Dict[str,
                                                                       Status]):
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
def create_absences(types: tp.Dict[str, AbsenceType],
                    statuses: tp.Dict[str, AbsenceStatus],
                    students: tp.Dict[str, Student]):
    values = [
        {
            'date': '2020-09-04',
            'student': students['Кацевалов'],
            'absence_type': types['Уважительная'],
            'reason': 'Заболел',
            'absence_status': statuses['Закрыт'],
            'comment': 'Болеть будет недолго'
        },
        {
            'date': '2020-09-11',
            'student': students['Хромов'],
            'absence_type': types['Опоздание'],
            'reason': 'Электричка опоздала',
            'absence_status': statuses['Закрыт'],
            'comment': ''
        },
        {
            'date': '2020-09-18',
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
def create_teachers(milgroups: tp.Dict[int, Milgroup],
                    milfaculties: tp.Dict[str, Milfaculty],
                    ranks: tp.Dict[str, Rank], posts: tp.Dict[str,
                                                              TeacherPost]):
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


def create_punishments(punishment_types: tp.Dict[str, PunishmentType],
                       students: tp.Dict[str, Student],
                       teachers: tp.Dict[str, Teacher]):
    values = [
        {
            'student': students['Хромов'],
            'reason': 'Не пришел на пары',
            'punishment_type': punishment_types['Взыскание'],
            'date': '2020-11-10',
            'teacher': teachers['Никандров'],
            'remove_date': '2020-11-13',
        },
        {
            'student': students['Исаков'],
            'reason': 'Сломал парту',
            'punishment_type': punishment_types['Выговор'],
            'date': '2020-11-12',
            'teacher': teachers['Репалов'],
            'remove_date': None,
        },
    ]

    for value in values:
        punishment, _ = Punishment.objects.get_or_create(**value)
        punishment.save()


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

    students = create_students(milgroups, programs, statuses)

    teachers = create_teachers(milgroups, milfaculties, ranks, posts)

    absence_types = create_absence_types()
    absence_statuses = create_absence_statuses()

    create_absences(absence_types, absence_statuses, students)

    punishment_types = create_punishment_types()
    create_punishments(punishment_types, students, teachers)

    return Response({'message': 'Population successful'},
                    status=HTTP_201_CREATED)
