from dms.models.common import (
    Author,
    Publisher,
)


def create_authors() -> list[Author]:
    data = [
        dict(surname="Кашин", name="Андрей", patronymic="Владимирович"),
        dict(surname="Никандров", name="Игорь", patronymic="Владимирович"),
        dict(surname="Пеляк", name="Виктор", patronymic="Степанович"),
        dict(surname="Репалов", name="Дмитрий", patronymic="Николаевич"),
        dict(surname="Усиков", name="Юрий", patronymic="Витальевич"),
    ]

    authors = []

    for fields in data:
        author, _ = Author.objects.get_or_create(**fields)
        authors.append(author)

    return authors


def create_publishers() -> list[Publisher]:
    data = [
        dict(name="Авиация"),
        dict(name="Космонавтика"),
        dict(name="Инженерный журнал"),
    ]

    publishers = []

    for fields in data:
        publisher, _ = Publisher.objects.get_or_create(**fields)
        publishers.append(publisher)

    return publishers
