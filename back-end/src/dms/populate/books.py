import random

from dms.models.common import Author
from dms.models.documents import File
from dms.models.papers import Publisher
from dms.models.class_materials import Subject
from dms.models.books import (
    Book,
    FavoriteBook,
)


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
        book, is_created = Book.objects.get_or_create(
            title=random.choice(titles),
            file=file,
            page_count=random.randint(100, 300),
        )

        if not is_created:
            continue

        for _ in range(random.randint(1, 2)):
            book.authors.add(random.choice(authors))

        for _ in range(random.randint(1, 2)):
            book.publishers.add(random.choice(publishers))

        for _ in range(random.randint(1, 2)):
            subj = random.choice(list(subjects.keys()))
            book.subjects.add(subjects[subj])

        book.save()
        books.append(book)

    return books


def create_favorite_books(
    books: list[Book],
    user,
) -> list[FavoriteBook]:
    favorites = []

    for book in books:
        favorite, _ = FavoriteBook.objects.get_or_create(book=book, user=user)
        favorites.append(favorite)

    return favorites
