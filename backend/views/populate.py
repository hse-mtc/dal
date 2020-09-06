import random

import typing as tp

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.views.decorators.csrf import csrf_exempt

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from backend.models import (
    Author,
    Category,
    Document,
    Profile,
    Publisher,
    Section,
    Subject,
    Topic,
)


def create_super_user() -> tp.Tuple[AbstractUser, Profile]:
    """
    Create super user "vspelyak" with password "qwerty".
    :return: User and Profile model instances.
    """

    user_model = get_user_model()

    if user_model.objects.filter(username="vspelyak").exists():
        return (user_model.objects.get(username="vspelyak"),
                Profile.objects.get(name="Пеляк В.С."))

    super_user = user_model.objects.create_superuser(
        username="vspelyak",
        password="qwerty",
    )
    super_user.save()

    profile, _ = Profile.objects.get_or_create(name="Пеляк В.С.",
                                               user=super_user)
    profile.save()

    return super_user, profile


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

    for last_name, first_name, patronymic in author_names:
        author, _ = Author.objects.get_or_create(
            last_name=last_name,
            first_name=first_name,
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

    subject_titles = [
        ("Тактическая подготовка", "ТП"),
        ("Тактико-специальная подготовка", "ТСП"),
        ("Военно-специальная подготовка", "ВСП"),
        ("Военно-инженерная подготовка", "ВИП"),
        ("Военно-политическая подготовка", "ВПП"),
        ("Военная топография", "ВТ"),
        ("Строевая подготовка", "СП"),
    ]

    for title, abbreviation in subject_titles:
        subject, _ = Subject.objects.get_or_create(
            title=title,
            abbreviation=abbreviation,
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
        "Лекции",
        "Семинары",
        "Практические занятия",
        "Групповые занятия",
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


def create_documents(
    authors: tp.List[Author],
    categories: tp.List[Category],
    publishers: tp.List[Publisher],
    subject: Subject,
    topics: tp.List[Topic],
) -> tp.List[Document]:
    """
    Create a bunch of documents for every category.
    :param authors: list of available authors.
    :param categories: list of available categories.
    :param publishers: list of available publishers.
    :param subject: subject to add document to.
    :param topics: list of available topics for document to add to.
    :return: list of created documents.
    """

    documents = []

    document_titles = [
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

    for i in range(25):
        document, is_created = Document.objects.get_or_create(
            title=random.choice(document_titles),
            category=random.choice(categories),
            file=ContentFile("some content here", name=f"document_id_{i}.txt"),
        )

        if not is_created:
            continue

        for _ in range(random.randint(1, 2)):
            document.authors.add(random.choice(authors))

        for _ in range(random.randint(1, 2)):
            document.publishers.add(random.choice(publishers))

        if document.category in categories[2:]:  # educational
            document.subject = subject
            document.topic = random.choice(topics)

        document.save()
        documents.append(document)

    return documents


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AllowAny,))
def populate(request: Request,) -> Response:
    """
    Populate database with fake documents, users, etc. (including super user).
    :param request: empty PUT request.
    :return: response indicating whether request was successful (probably was).
    """

    create_super_user()

    authors = create_authors()
    categories = create_categories()
    publishers = create_publishers()
    subjects = create_subjects()

    sections = create_sections(subjects[0])
    topics = create_topics(sections[0])

    create_documents(
        authors=authors,
        categories=categories,
        publishers=publishers,
        subject=subjects[0],
        topics=topics,
    )

    return Response(status=HTTP_200_OK)
