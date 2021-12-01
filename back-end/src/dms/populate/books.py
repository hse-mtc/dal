import random

from django.contrib.auth import get_user_model

from common.utils.populate import get_or_create

from dms.models.common import Author
from dms.models.documents import File
from dms.models.papers import Publisher
from dms.models.class_materials import Subject
from dms.models.books import (
    Book,
    FavoriteBook,
)


User = get_user_model()


def create_books(
    authors: list[Author],
    files: list[File],
    publishers: list[Publisher],
    subjects: list[Subject],
) -> list[Book]:
    # pylint: disable=too-many-arguments,too-many-locals

    random.seed(11)

    books = []

    titles = [
        "Учебник по ТСП",
        "Физика для ракетчиков",
        "Сферическая геометрия",
        "Пособие по танкам",
        "Тактическая подготовка",
        "Рукопашный бой под водой",
    ]

    for file in files:
        fields = dict(
            title=random.choice(titles),
            file=file,
            page_count=random.randint(100, 300),
        )
        book = get_or_create(Book, **fields)

        for _ in range(random.randint(1, 2)):
            book.authors.add(random.choice(authors))
        for _ in range(random.randint(1, 2)):
            book.publishers.add(random.choice(publishers))
        for _ in range(random.randint(1, 2)):
            book.subjects.add(random.choice(subjects))
        book.save()

        books.append(book)

    return books


def create_favorite_books(
    books: list[Book],
    user: User,
) -> list[FavoriteBook]:
    return [
        get_or_create(FavoriteBook, **dict(book=book, user=user))
        for book in books
    ]
