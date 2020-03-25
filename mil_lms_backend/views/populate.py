import typing as tp

from django.contrib.auth.models import User

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.decorators import api_view

from mil_lms_backend.models import (
    Status,
    Program,
    Milgroup,
    Milfaculty,
    Student
)


def create_statuses() -> tp.Dict[str, Status]:
    values = [
        'Завершил', 'Обучается', 'Отчислен'
    ]
    statuses = {}

    for value in values:
        status, _ = Status.objects.get_or_create(
            status=value
        )
        status.save()
        statuses[value] = status

    return statuses


def create_programs() -> tp.Dict[str, Program]:
    values = [
        {'code': '09.03.01', 'program': 'Информатика и вычислительная техника'},
        {'code': '09.03.04', 'program': 'Программная инженерия'},
        {'code': '15.03.01', 'program': 'Машиностроение'},
        {'code': '45.03.04', 'program': 'Интеллектуальные системы в гуманитарной сфере'}
    ]
    programs = {}

    for value in values:
        program, _ = Program.objects.get_or_create(
            code=value['code'],
            program=value['program']
        )
        program.save()
        programs[value['program']] = program

    return programs


def create_milfaculties() -> tp.Dict[str, Milfaculty]:
    values = [
        'ВКС', 'Сержанты', 'Разведка', 'РВСН'
    ]
    milfaculties = {}

    for value in values:
        milfaculty, _ = Milfaculty.objects.get_or_create(
            milfaculty=value
        )
        milfaculty.save()
        milfaculties[value] = milfaculty

    return milfaculties


def create_milgroups(milfaculties: tp.Dict[str, Milfaculty]) -> tp.Dict[str, Milgroup]:
    values = [
        {'milgroup': 1801, 'milfaculty': milfaculties['Разведка']},
        {'milgroup': 1802, 'milfaculty': milfaculties['Разведка']},
        {'milgroup': 1803, 'milfaculty': milfaculties['Разведка']},
        {'milgroup': 1804, 'milfaculty': milfaculties['Сержанты']},
        {'milgroup': 1805, 'milfaculty': milfaculties['Сержанты']},
        {'milgroup': 1806, 'milfaculty': milfaculties['Сержанты']},
        {'milgroup': 1807, 'milfaculty': milfaculties['ВКС']},
        {'milgroup': 1808, 'milfaculty': milfaculties['ВКС']},
        {'milgroup': 1809, 'milfaculty': milfaculties['ВКС']},
        {'milgroup': 1810, 'milfaculty': milfaculties['РВСН']},
        {'milgroup': 1811, 'milfaculty': milfaculties['РВСН']},
        {'milgroup': 1812, 'milfaculty': milfaculties['РВСН']}
    ]
    milgroups = {}

    for value in values:
        milgroup, _ = Milgroup.objects.get_or_create(
            milgroup=value['milgroup'],
            milfaculty=value['milfaculty']
        )
        milgroup.save()
        milgroups[value['milgroup']] = milgroup

    return milgroups


def create_students(milgroups: tp.Dict[int, Milgroup],
                    programs: tp.Dict[str, Program],
                    statuses: tp.Dict[str, Status]):
    values = [
        {
            'surname': 'Хромов',
            'name': 'Григорий',
            'patronymic': 'Александрович',
            'milgroup': milgroups[1809],
            'birthdate': '2000-11-04',
            'program': programs['Информатика и вычислительная техника'],
            'status': statuses['Обучается'],
            'photo': None
        },
        {
            'surname': 'Кацевалов',
            'name': 'Артем',
            'patronymic': 'Сергеевич',
            'milgroup': milgroups[1809],
            'birthdate': '2000-02-23',
            'program': programs['Информатика и вычислительная техника'],
            'status': statuses['Обучается'],
            'photo': None
        },
        {
            'surname': 'Исаков',
            'name': 'Владислав',
            'patronymic': 'Евгеньевич',
            'milgroup': milgroups[1809],
            'birthdate': '1999-08-29',
            'program': programs['Информатика и вычислительная техника'],
            'status': statuses['Обучается'],
            'photo': None
        },
        {
            'surname': 'Алиев',
            'name': 'Насир',
            'patronymic': 'Ашурович',
            'milgroup': milgroups[1808],
            'birthdate': '1999-05-14',
            'program': programs['Информатика и вычислительная техника'],
            'status': statuses['Обучается'],
            'photo': None
        },
        {
            'surname': 'Куркин',
            'name': 'Андрей',
            'patronymic': 'Витальевич',
            'milgroup': milgroups[1812],
            'birthdate': '1999-11-12',
            'program': programs['Информатика и вычислительная техника'],
            'status': statuses['Обучается'],
            'photo': None
        },
        {
            'surname': 'Иванов',
            'name': 'Петр',
            'patronymic': 'Сидорович',
            'milgroup': milgroups[1804],
            'birthdate': '1999-05-04',
            'program': programs['Машиностроение'],
            'status': statuses['Отчислен'],
            'photo': None
        },
        {
            'surname': 'Чукмарикадзе',
            'name': 'Губарибек',
            'patronymic': 'Алкинбеков',
            'milgroup': milgroups[1801],
            'birthdate': '1969-04-13',
            'program': programs['Интеллектуальные системы в гуманитарной сфере'],
            'status': statuses['Завершил'],
            'photo': None
        }
    ]

    for value in values:
        student, _ = Student.objects.get_or_create(
            surname=value['surname'],
            name=value['name'],
            patronymic=value['patronymic'],
            milgroup=value['milgroup'],
            birthdate=value['birthdate'],
            program=value['program'],
            status=value['status'],
            photo=value['photo']
        )
        student.save()


@api_view(['PUT'])
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

    create_students(milgroups, programs, statuses)

    return Response({'message': 'Population successful'}, status=HTTP_201_CREATED)
