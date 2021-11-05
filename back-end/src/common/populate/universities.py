from common.models.universities import (
    Campus,
    Faculty,
    Program,
)

from common.utils.populate import get_or_create


def create_faculties() -> dict[str, Faculty]:
    faculties = [
        {
            "campus": Campus.MOSCOW.value,
            "title": "Московский институт электроники и математики им. А.Н. Тихонова",
            "abbreviation": "МИЭМ",
        },
        {
            "campus": Campus.MOSCOW.value,
            "title": "Факультет экономических наук",
            "abbreviation": "ФЭН",
        },
        {
            "campus": Campus.MOSCOW.value,
            "title": "Факультет компьютерных наук",
            "abbreviation": "ФКН",
        },
    ]

    return {
        fields["abbreviation"]: get_or_create(Faculty, **fields)
        for fields in faculties
    }


def create_programs(faculties: dict[str, Faculty]) -> dict[str, Program]:
    programs = [
        {
            "code": "09.03.01 Информатика и вычислительная техника",
            "title": "Информатика и вычислительная техника",
            "faculty": faculties["МИЭМ"]
        },
        {
            "code": "10.03.01 Информационная безопасность",
            "title": "Информационная безопасность",
            "faculty": faculties["МИЭМ"],
        },
        {
            "code": "38.03.01 Экономика",
            "title": "Экономика",
            "faculty": faculties["ФКН"],
        },
        {
            "code": "09.03.04 Программная инженерия",
            "title": "Программная инженерия",
            "faculty": faculties["ФКН"],
        },
    ]

    return {
        fields["title"]: get_or_create(Program, **fields)
        for fields in programs
    }
