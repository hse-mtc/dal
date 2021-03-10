import random

from dms.models.common import Author
from dms.models.documents import File
from dms.models.papers import (
    Category,
    Paper,
    Publisher,
)


def create_categories() -> list[Category]:
    data = [
        dict(title="Научные статьи"),
        dict(title="Научно-исследовательские работы"),
        dict(title="Приказы Министерства образования"),
    ]

    categories = []

    for fields in data:
        category, _ = Category.objects.get_or_create(**fields)
        categories.append(category)

    return categories


def create_papers(
    authors: list[Author],
    categories: list[Category],
    publishers: list[Publisher],
    files: list[File],
) -> list[Paper]:
    # pylint: disable=too-many-arguments,too-many-locals
    random.seed(54321)

    papers = []

    titles = [
        "Техники обеспечения",
        "Управление войсками",
        "Виды угроз",
        "Исследование обезоруживания",
        "Авиаследы",
        "Эпидемия среди своих",
        "Противник в тылу",
        "Снег летом",
        "Пурга в пустыне",
        "Угроза в отражении",
    ]

    for file in files:
        paper, is_created = Paper.objects.get_or_create(
            title=random.choice(titles),
            category=random.choice(categories),
            file=file,
        )

        if not is_created:
            continue

        for _ in range(random.randint(1, 2)):
            paper.authors.add(random.choice(authors))

        for _ in range(random.randint(1, 2)):
            paper.publishers.add(random.choice(publishers))

        papers.append(paper)

    return papers
