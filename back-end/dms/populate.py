import random

import typing as tp

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from auth.models import Profile

from dms.models import (
    Author,
    Book,
    Category,
    ClassMaterial,
    File,
    Paper,
    Publisher,
    Section,
    Subject,
    Topic,
)


User = get_user_model()


def create_super_user():
    if User.objects.filter(username="vspelyak").exists():
        return

    super_user = User.objects.create_superuser(
        username="vspelyak",
        password="qwerty",
    )
    super_user.save()

    profile, _ = Profile.objects.get_or_create(
        surname="Пеляк",
        name="Виктор",
        patronymic="Степанович",
        user=super_user,
    )
    profile.save()


def create_test_user():
    if User.objects.filter(username="test").exists():
        return

    test_user = User.objects.create_user(
        username="test",
        password="qwerty",
        is_staff=True,
    )
    test_user.save()

    profile, _ = Profile.objects.get_or_create(
        surname="Фамилия",
        name="Имя",
        patronymic="Отчество",
        user=test_user,
    )
    profile.save()


def create_users():
    """Create some mock users.

    Create super user "vspelyak" with password "qwerty"
    and regular user "test" with password "test".
    """

    create_super_user()
    create_test_user()


def create_authors() -> tp.List[Author]:
    """
    Create authors with names from "authors_name".
    :return: list of created authors.
    """

    authors = []

    author_names = [
        ("Кашин", "Андрей", "Владимирович"),
        ("Никандров", "Игорь", "Владимирович"),
        ("Пеляк", "Виктор", "Степанович"),
        ("Репалов", "Дмитрий", "Николаевич"),
        ("Усиков", "Юрий", "Витальевич"),
    ]

    for surname, name, patronymic in author_names:
        author, _ = Author.objects.get_or_create(
            surname=surname,
            name=name,
            patronymic=patronymic,
        )
        author.save()
        authors.append(author)

    return authors


def create_subjects() -> tp.List[Subject]:
    """
    Create subjects with titles from "subject_titles".
    :return: list of created subjects.
    """

    subjects = []

    titles = [
        "Тактическая подготовка",
        "Тактико-специальная подготовка",
        "Военно-специальная подготовка",
        "Военно-инженерная подготовка",
        "Военно-политическая подготовка",
        "Военная топография",
        "Строевая подготовка",
    ]

    for title in titles:
        subject, _ = Subject.objects.get_or_create(
            title=title,
            annotation=f"Пример аннотации для {title.lower()}",
        )
        subject.save()
        subjects.append(subject)

    return subjects


def create_publishers() -> tp.List[Publisher]:
    """
    Create publishers with names from "publisher_names".
    :return: list of created publishers.
    """

    publishers = []

    publisher_names = [
        "Авиация",
        "Космонавтика",
        "Инженерный журнал",
    ]

    for name in publisher_names:
        publisher, _ = Publisher.objects.get_or_create(name=name,)
        publisher.save()
        publishers.append(publisher)

    return publishers


def create_categories() -> tp.List[Category]:
    """
    Create categories with titles from "category_titles".
    :return: list of created categories.
    """

    categories = []

    category_titles = [
        "Научные статьи",
        "Научно-исследовательские работы",
        "Приказы Министерства образования",
    ]

    for title in category_titles:
        category, _ = Category.objects.get_or_create(title=title,)
        category.save()
        categories.append(category)

    return categories


def create_sections(subject: Subject) -> tp.List[Section]:
    """
    Create sections for particular subject.
    :param subject: Subject model (preferably from "create_subjects").
    :return: list of created sections.
    """

    sections = []

    section_titles = [
        "Виды и рода войск",
        "Основы современного боя",
        "Действия солдата в бою",
        "Штатная структура",
        "Отделение в разведке",
    ]

    for title in section_titles:
        section, _ = Section.objects.get_or_create(
            title=title,
            subject=subject,
        )
        section.save()
        sections.append(section)

    return sections


def create_topics(section: Section,) -> tp.List[Topic]:
    """
    Create topics for particular section.
    :param section: Section model (preferably from "create_sections").
    :return: list of created topics.
    """

    topics = []

    topic_titles = [
        "Механизированные войска",
        "Ракетные войска и артиллерия",
        "Войсковая противовоздушная оборона",
        "Специальные войска",
    ]

    for title in topic_titles:
        topic, _ = Topic.objects.get_or_create(
            title=title,
            section=section,
        )
        topic.save()
        topics.append(topic)

    return topics


def create_files() -> tp.List[File]:
    files = []

    for i in range(25):
        name = f"document_id_{i}.txt"
        content = ContentFile("some content here", name=name)
        file = File.objects.create(content=content, name=name)
        file.save()
        files.append(file)

    return files


def create_papers(
    authors: tp.List[Author],
    categories: tp.List[Category],
    publishers: tp.List[Publisher],
    files: tp.List[File],
) -> tp.List[Paper]:
    """
    Create a bunch of documents for every category.
    :param authors: list of available authors.
    :param categories: list of available categories.
    :param publishers: list of available publishers.
    :param files: list of uploaded files.
    :return: list of created papers.
    """

    # pylint: disable=too-many-arguments,too-many-locals

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

    random.seed(11)

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

        paper.save()
        papers.append(paper)

    return papers


def create_class_materials(files, topics):
    materials = []

    titles = [
        "Контрольная работа",
        "Новый материал",
        "Исследовательский проект",
        "Научные методы",
        "Управление персоналом",
    ]

    for file in files:
        material, is_created = ClassMaterial.objects.get_or_create(
            title=random.choice(titles),
            file=file,
            type=random.choice(ClassMaterial.Type.values),
            topic=random.choice(topics),
        )

        if not is_created:
            continue

        material.save()
        materials.append(material)

    return materials


def create_books(authors, files, publishers, subjects):
    # pylint: disable=too-many-arguments,too-many-locals

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
        )

        if not is_created:
            continue

        for _ in range(random.randint(1, 2)):
            book.authors.add(random.choice(authors))

        for _ in range(random.randint(1, 2)):
            book.publishers.add(random.choice(publishers))

        for _ in range(random.randint(1, 2)):
            book.subjects.add(random.choice(subjects))

        book.save()
        books.append(book)

    return books


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def populate(request: Request) -> Response:
    # pylint: disable=too-many-locals

    create_users()

    authors = create_authors()
    categories = create_categories()
    publishers = create_publishers()
    subjects = create_subjects()
    files = create_files()

    sections = create_sections(subjects[0])
    topics = create_topics(sections[0])

    create_papers(
        authors=authors,
        categories=categories,
        publishers=publishers,
        files=files,
    )
    create_class_materials(
        files=files,
        topics=topics,
    )
    create_books(
        authors=authors,
        files=files,
        publishers=publishers,
        subjects=subjects,
    )

    return Response(status=HTTP_200_OK)
