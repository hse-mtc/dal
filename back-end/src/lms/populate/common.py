from common.utils.populate import get_or_create

from lms.models.common import Milfaculty, Milgroup, Milspecialty


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
    milfaculties: dict[str, Milfaculty], milspecialties: dict[str, Milspecialty]
) -> dict[str, Milgroup]:
    milgroups = [
        {
            "title": "1801",
            "milfaculty": milfaculties["Разведка"],
            "milspecialty": milspecialties["094001"],
            "weekday": 4,
        },
        {
            "title": "1802",
            "milfaculty": milfaculties["Разведка"],
            "milspecialty": milspecialties["094001"],
            "weekday": 4,
        },
        {
            "title": "1803",
            "milfaculty": milfaculties["Разведка"],
            "milspecialty": milspecialties["094001"],
            "weekday": 4,
        },
        {
            "title": "1804",
            "milfaculty": milfaculties["Сержанты"],
            "milspecialty": milspecialties["100182"],
            "weekday": 4,
        },
        {
            "title": "1805",
            "milfaculty": milfaculties["Сержанты"],
            "milspecialty": milspecialties["100182"],
            "weekday": 4,
        },
        {
            "title": "1806",
            "milfaculty": milfaculties["Сержанты"],
            "milspecialty": milspecialties["100182"],
            "weekday": 4,
        },
        {
            "title": "1807",
            "milfaculty": milfaculties["ВКС"],
            "milspecialty": milspecialties["453100"],
            "weekday": 4,
        },
        {
            "title": "1808",
            "milfaculty": milfaculties["ВКС"],
            "milspecialty": milspecialties["453100"],
            "weekday": 4,
        },
        {
            "title": "1809",
            "milfaculty": milfaculties["ВКС"],
            "milspecialty": milspecialties["453100"],
            "weekday": 4,
        },
        {
            "title": "1810",
            "milfaculty": milfaculties["РВСН"],
            "milspecialty": milspecialties["411300"],
            "weekday": 4,
        },
        {
            "title": "1811",
            "milspecialty": milspecialties["411300"],
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1812",
            "milspecialty": milspecialties["411300"],
            "milfaculty": milfaculties["РВСН"],
            "weekday": 4,
        },
        {
            "title": "1612",
            "milspecialty": milspecialties["411300"],
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
