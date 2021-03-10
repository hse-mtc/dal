import random

from dms.models.documents import File
from dms.models.class_materials import (
    Section,
    Topic,
    ClassMaterial,
)

from common.models.subjects import Subject


def create_sections(subject: Subject) -> list[Section]:
    sections = []

    titles = [
        "Виды и рода войск",
        "Основы современного боя",
        "Действия солдата в бою",
        "Штатная структура",
        "Отделение в разведке",
    ]

    for title in titles:
        section, _ = Section.objects.get_or_create(
            title=title,
            subject=subject,
        )
        sections.append(section)

    return sections


def create_topics(section: Section) -> list[Topic]:
    topics = []

    titles = [
        "Механизированные войска",
        "Ракетные войска и артиллерия",
        "Войсковая противовоздушная оборона",
        "Специальные войска",
    ]

    for title in titles:
        topic, _ = Topic.objects.get_or_create(
            title=title,
            annotation=f"Пример аннотации для {title}",
            section=section,
        )
        topics.append(topic)

    return topics


def create_class_materials(
    files: list[File],
    topics: list[Topic],
) -> list[ClassMaterial]:
    random.seed(342)

    materials = []

    titles = [
        "Контрольная работа",
        "Новый материал",
        "Исследовательский проект",
        "Научные методы",
        "Управление персоналом",
    ]

    for file in files:
        material, _ = ClassMaterial.objects.get_or_create(
            title=random.choice(titles),
            file=file,
            type=random.choice(ClassMaterial.Type.values),
            topic=random.choice(topics),
        )
        materials.append(material)

    return materials
