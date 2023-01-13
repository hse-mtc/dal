from common.utils.populate import get_or_create

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


def create_milfaculties() -> dict[str, Milfaculty]:
    milfaculties = [
        {
            "title": "Воздушно-космические силы",
            "abbreviation": "ВКС",
        },
        {
            "title": "Сержанты",
            "abbreviation": "Сержанты",
        },
        {
            "title": "Разведка",
            "abbreviation": "Разведка",
        },
        {
            "title": "Ракетные войска стратегического назначения",
            "abbreviation": "РВСН",
        },
        {
            "title": "Офицеры ЗИТ",
            "abbreviation": "ЗИТ",
        },
        {
            "title": "Беспилотные летательные аппараты",
            "abbreviation": "БПЛА",
        },
    ]

    return {
        fields["abbreviation"]: get_or_create(Milfaculty, **fields)
        for fields in milfaculties
    }


def create_milgroups(
    milfaculties: dict[str, Milfaculty],
) -> dict[str, Milgroup]:
    milgroups = [
        {
            "title": "1801",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1802",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1803",
            "milfaculty": milfaculties["Разведка"],
            "weekday": 4,
        },
        {
            "title": "1804",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1805",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1806",
            "milfaculty": milfaculties["Сержанты"],
            "weekday": 4,
        },
        {
            "title": "1807",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1808",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1809",
            "milfaculty": milfaculties["ВКС"],
            "weekday": 4,
        },
        {
            "title": "1810",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1811",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1812",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1612",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
        {
            "title": "1813",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
        {
            "title": "1814",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
        {
            "title": "1614",
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
            "archived": True,
        },
    ]

    return {fields["title"]: get_or_create(Milgroup, **fields) for fields in milgroups}
