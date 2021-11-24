import random

from common.models.subjects import Subject

from common.utils.populate import get_or_create

from dms.models.documents import File
from dms.models.class_materials import (
    Section,
    Topic,
    ClassMaterial,
)



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
        fields = dict(
            title=title,
            subject=subject,
        )
        section = get_or_create(Section, **fields)
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
        fields = dict(
            title=title,
            annotation=f"Пример аннотации для {title}",
            section=section,
        )
        topic = get_or_create(Topic, **fields)
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
        fields = dict(
            title=random.choice(titles),
            file=file,
            type=random.choice(ClassMaterial.Type.values),
            topic=random.choice(topics),
        )
        material = get_or_create(ClassMaterial, **fields)
        materials.append(material)

    return materials
