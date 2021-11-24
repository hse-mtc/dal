from common.utils.populate import get_or_create

from dms.models.common import (
    Author,
    Publisher,
)


def create_authors() -> list[Author]:
    authors = [
        dict(surname="Кашин", name="Андрей", patronymic="Владимирович"),
        dict(surname="Никандров", name="Игорь", patronymic="Владимирович"),
        dict(surname="Пеляк", name="Виктор", patronymic="Степанович"),
        dict(surname="Репалов", name="Дмитрий", patronymic="Николаевич"),
        dict(surname="Усиков", name="Юрий", patronymic="Витальевич"),
    ]

    return [
        get_or_create(Author, **fields)
        for fields in authors
    ]


def create_publishers() -> list[Publisher]:
    publishers = [
        dict(name="Авиация"),
        dict(name="Космонавтика"),
        dict(name="Инженерный журнал"),
    ]

    return [
        get_or_create(Publisher, **fields)
        for fields in publishers
    ]
