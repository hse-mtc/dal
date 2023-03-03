from common.models.subjects import Subject
from common.models.milspecialties import Milspecialty
from common.utils.populate import get_or_create


def create_subjects(milspecialties: dict[str, Milspecialty]) -> list[Subject]:
    subjects = [
        {
            "title": "Военная топография",
            "milspecialty": milspecialties["100182"],
            "annotation": "Дисциплина военного дела, изучающая методы и \
                средства оценки местности, ориентирования на местности и \
                    осуществления полевых измерений для обеспечения боевой \
                        деятельности войск (сил), определяющая правила по \
                            ведению рабочих карт командиров и разработки \
                                графических боевых документов.",
        },
        {
            "title": "Огневая подготовка",
            "milspecialty": milspecialties["453000"],
            "annotation": "Предмет обучения военнослужащих применению штатного \
                оружия для поражения различных целей в бою.",
        },
        {
            "title": "Тактическая подготовка",
            "milspecialty": milspecialties["453000"],
            "annotation": "Предмет обучения военнослужащих подготовке \
                и ведению боя.",
        },
        {
            "title": "Строевая подготовка",
            "milspecialty": milspecialties["453000"],
            "annotation": "Предмет обучения военнослужащих и \
                подразделений умению выполнять команды, строевые \
                    приёмы с оружием и без оружия.",
        },
        {
            "title": "Общевоинские уставы ВС РФ",
            "milspecialty": milspecialties["453000"],
            "annotation": "Предмет обучения военнослужащих сути и содержанию \
                общевоинских Уставов ВС РФ.",
        },
    ]

    return [get_or_create(Subject, **fields) for fields in subjects]
