from common.models.universities import Campus
from common.models.milspecialties import Milspecialty

from common.utils.populate import get_or_create


def create_milspecialties() -> dict[str, Milspecialty]:
    milspecialties = [
        {
            "code": "453000",
            "title": "Организация эксплуатации и ремонта автоматизированных систем управления и вычислительных комплексов ракетно-космической обороны",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "453100",
            "title": "Математическое и программное обеспечение функционирования вычислительных комплексов ракетно-космической обороны",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "461300",
            "title": "Эксплуатация и ремонт радиоэлектронного оборудования самолетов, вертолетов и авиационных ракет",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "094001",
            "title": "Применение наземных подразделений войсковой разведки",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "411300",
            "title": "Эксплуатация и ремонт автоматизированных систем комплексов баллистических стратегических ракет наземного базирования",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "751100",
            "title": "Защита информационных технологий",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "100182",
            "title": "Стрелковые, командир стрелкового отделения",
            "available_for": [Campus.MOSCOW.value],
        },
        {
            "code": "106646-543",
            "title": "Разведывательные, разведчик-оператор СБР, ПСНР",
            "available_for": [Campus.SAINT_PETERSBURG.value, Campus.NIZHNY_NOVGOROD.value, Campus.PERM.value],
        },
    ]

    return {
        fields["code"]: get_or_create(Milspecialty, **fields)
        for fields in milspecialties
    }
