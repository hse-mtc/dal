import random

from common.utils.populate import get_or_create

from dms.models.common import Author
from dms.models.documents import File
from dms.models.papers import (
    Category,
    Paper,
    Publisher,
)


def create_categories() -> list[Category]:
    categories = [
        dict(title="Научные статьи"),
        dict(title="Научно-исследовательские работы"),
        dict(title="Приказы Министерства образования"),
    ]

    return [get_or_create(Category, **fields) for fields in categories]


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
        fields = dict(
            title=random.choice(titles),
            category=random.choice(categories),
            file=file,
        )

        paper = get_or_create(Paper, **fields)

        for _ in range(random.randint(1, 2)):
            paper.authors.add(random.choice(authors))

        for _ in range(random.randint(1, 2)):
            paper.publishers.add(random.choice(publishers))

        papers.append(paper)

    return papers
