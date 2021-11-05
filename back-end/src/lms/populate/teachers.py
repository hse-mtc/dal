from django.contrib.auth import get_user_model

from common.utils.populate import get_or_create

from lms.models.teachers import Teacher
from lms.models.common import (
    Milfaculty,
    Milgroup,
)


User = get_user_model()


def create_teachers(
    milgroups: dict[str, Milgroup],
    milfaculties: dict[str, Milfaculty],
    users: dict[str, User],
) -> dict[str, Teacher]:
    teachers = [
        {
            "surname": "Никандров",
            "name": "Игорь",
            "patronymic": "Владимирович",
            "user": users["ivnikandrov@mail.com"],
            "milfaculty": milfaculties["ВКС"],
            "milgroups": [milgroups["1809"]],

            "post": Teacher.Post.TEACHERS.value,
            "rank": Teacher.Rank.LIEUTENANT_COLONEL.value,
        },
        {
            "surname": "Репалов",
            "name": "Дмитрий",
            "patronymic": "Николаевич",
            "user": users["dnrepalov@mail.com"],
            "milfaculty": milfaculties["ВКС"],
            "milgroups": [milgroups["1808"], milgroups["1809"]],

            "post": Teacher.Post.MILFACULTY_HEAD.value,
            "rank": Teacher.Rank.LIEUTENANT_COLONEL.value,
        },
        {
            "surname": "Мещеряков",
            "name": "Иван",
            "patronymic": "Владимирович",
            "user": users["ivmesheryakov@mail.com"],
            "milfaculty": milfaculties["Сержанты"],
            "milgroups": [milgroups["1806"]],

            "post": Teacher.Post.TEACHERS.value,
            "rank": Teacher.Rank.MAJOR.value,
        },
        {
            "surname": "Ковальчук",
            "name": "Игорь",
            "patronymic": "Валентинович",
            "user": users["ivkovalchuk@mail.com"],
            "milfaculty": milfaculties["Разведка"],
            "milgroups": [milgroups["1801"]],

            "post": Teacher.Post.MILFACULTY_HEAD.value,
            "rank": Teacher.Rank.COLONEL.value,
        },
        {
            "surname": "Гаврилов",
            "name": "Климент",
            "patronymic": "Сергеевич",
            "user": users["ksgavrilov@mail.com"],
            "milfaculty": milfaculties["РВСН"],
            "milgroups": [],

            "post": Teacher.Post.TEACHERS.value,
            "rank": Teacher.Rank.MAJOR_GENERAL.value,
        },
    ]

    objects = {}

    for fields in teachers:
        milgroups = fields.pop("milgroups")

        object_ = get_or_create(Teacher, **fields)

        object_.milgroups.add(*milgroups)
        object_.save()

        objects[fields["surname"]] = object_

    return objects
