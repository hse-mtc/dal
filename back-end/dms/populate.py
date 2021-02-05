import random

import typing as tp

from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    permission_classes,
)

from auth.models import Profile

from dms.models.books import Book
from dms.models.documents import File
from dms.models.papers import (
    Category,
    Paper,
)
from dms.models.class_materials import (
    ClassMaterial,
    Section,
    Topic,
)
from dms.models.common import (
    Author,
    Publisher,
    User,
)

from common.models.subjects import Subject


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


def create_test_users():
    if not User.objects.filter(username="test").exists():
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

    if not User.objects.filter(username="student").exists():
        test_user = User.objects.create_user(
            username="student",
            password="qwerty",
            is_staff=True,
        )
        test_user.save()

        profile, _ = Profile.objects.get_or_create(
            surname="Студентов",
            name="Студент",
            patronymic="Студентович",
            user=test_user,
        )
        profile.save()

    if not User.objects.filter(username="teacher").exists():
        test_user = User.objects.create_user(
            username="teacher",
            password="qwerty",
            is_staff=True,
        )
        test_user.save()

        profile, _ = Profile.objects.get_or_create(
            surname="Преподов",
            name="Препод",
            patronymic="Преподович",
            user=test_user,
        )
        profile.save()

    if not User.objects.filter(username="milfaculty_head").exists():
        test_user = User.objects.create_user(
            username="milfaculty_head",
            password="qwerty",
            is_staff=True,
        )
        test_user.save()

        profile, _ = Profile.objects.get_or_create(
            surname="Начальников",
            name="Начальник",
            patronymic="Начальникович",
            user=test_user,
        )
        profile.save()


def create_users():
    """Create some mock users.

    Create super user "vspelyak" with password "qwerty"
    and regular user "test" with password "test".
    """

    create_super_user()
    create_test_users()


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
        category, _ = Category.objects.get_or_create(title=title)
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
            annotation=f"Пример аннотации для {title}",
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
            page_count=random.randint(100, 300),
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


def create_permissions_for_a_view(view_name, view_name_rus):
    get_str = ": получение данных"
    post_str = ": добавление данных"
    patch_str = ": редактирование данных"
    delete_str = ": удаление данных"

    return [
        {
            "codename": view_name + "_get",
            "name": view_name_rus + get_str,
        },
        {
            "codename": view_name + "_post",
            "name": view_name_rus + post_str,
        },
        {
            "codename": view_name + "_patch",
            "name": view_name_rus + patch_str,
        },
        {
            "codename": view_name + "_delete",
            "name": view_name_rus + delete_str,
        },
    ]


def create_permissions(content_type):

    values = []
    values += create_permissions_for_a_view("student", "Студенты")
    values += create_permissions_for_a_view("teacher", "Учителя")
    values += create_permissions_for_a_view("absence", "Пропуски")
    values += create_permissions_for_a_view("achievement", "Достижения")
    values += create_permissions_for_a_view("encouragement", "Поощрения")
    values += create_permissions_for_a_view("punishment", "Взыскания")
    values += create_permissions_for_a_view("subject", "Предметы")
    values += create_permissions_for_a_view("lesson", "Расписание занятий")
    values += create_permissions_for_a_view("mark", "Оценки")
    values += create_permissions_for_a_view("reference_book",
                                            "Справочные данные")
    for val in values:
        Permission.objects.get_or_create(codename=val["codename"],
                                         name=val["name"],
                                         content_type=content_type)


def get_student_permissions():
    values = [
        "student_get",
        "teacher_get",
        "absence_get",
        "achievement_get",
        "encouragement_get",
        "punishment_get",
        "subject_get",
        "lesson_get",
        "mark_get",
        "reference_book_get",
    ]
    return [Permission.objects.get(codename=val) for val in values]


def get_teacher_permissions():
    values = [
        "student_get",
        "teacher_get",
        "absence_get",
        "achievement_get",
        "achievement_post",
        "achievement_patch",
        "encouragement_get",
        "encouragement_post",
        "encouragement_patch",
        "punishment_get",
        "punishment_post",
        "punishment_patch",
        "subject_get",
        "subject_post",
        "subject_patch",
        "subject_delete",
        "lesson_get",
        "lesson_post",
        "lesson_patch",
        "lesson_delete",
        "mark_get",
        "mark_post",
        "mark_patch",
        "mark_delete",
        "reference_book_get",
    ]
    return [Permission.objects.get(codename=val) for val in values]


def get_milfaculty_head_permissions():
    values = [
        "student_get",
        "student_post",
        "student_patch",
        "student_delete",
        "teacher_get",
        "teacher_post",
        "teacher_patch",
        "teacher_delete",
        "absence_get",
        "absence_post",
        "absence_patch",
        "absence_delete",
        "achievement_get",
        "achievement_post",
        "achievement_patch",
        "achievement_delete",
        "encouragement_get",
        "encouragement_post",
        "encouragement_patch",
        "encouragement_delete",
        "punishment_get",
        "punishment_post",
        "punishment_patch",
        "punishment_delete",
        "subject_get",
        "subject_post",
        "subject_patch",
        "subject_delete",
        "lesson_get",
        "lesson_post",
        "lesson_patch",
        "lesson_delete",
        "mark_get",
        "mark_post",
        "mark_patch",
        "mark_delete",
        "reference_book_get",
        "reference_book_post",
        "reference_book_patch",
        "reference_book_delete",
    ]
    return [Permission.objects.get(codename=val) for val in values]


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def populate(request: Request) -> Response:
    # pylint: disable=too-many-locals

    create_users()

    # create groups and permissions
    students, _ = Group.objects.get_or_create(name="students")
    teachers, _ = Group.objects.get_or_create(name="teachers")
    milfaculty_heads, _ = Group.objects.get_or_create(name="milfaculty_heads")
    content_type = ContentType.objects.get_for_model(Group)

    create_permissions(content_type)

    students.permissions.set(get_student_permissions())
    teachers.permissions.set(get_teacher_permissions())
    milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

    students.user_set.add(User.objects.get(username="student"))
    teachers.user_set.add(User.objects.get(username="teacher"))
    milfaculty_heads.user_set.add(User.objects.get(username="milfaculty_head"))

    # other dms models population
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
