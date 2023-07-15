from common.models.subjects import Subject

from common.utils.populate import get_or_create


def create_subjects(milspecialties: dict) -> list[Subject]:
    milspecialties_codes = ["453000", "453100", "461300", "094001", "411300"]
    milspecialties = {code: milspecialties[code] for code in milspecialties_codes}
    subjects = [
        {
            "title": "Тактическая подготовка",
            "annotation": "Описание ТП",
        },
        {
            "title": "Тактико-специальная подготовка",
            "annotation": "Описание ТСП",
        },
        {
            "title": "Военно-специальная подготовка",
            "annotation": "Описание ВСП",
        },
        {
            "title": "Военно-политическая подготовка",
            "annotation": "Описание ВПП",
        },
        {
            "title": "Военная топография",
            "annotation": "Описание ВТ",
        },
        {
            "title": "Строевая подготовка",
            "annotation": "Описание Стр.п",
        },
    ]
    subjects_final = []
    for subject in subjects:
        for milspecialty in milspecialties:
            subjects_final.append(subject.copy())
            subjects_final[-1].update({"milspecialty": milspecialties[milspecialty]})

    return [get_or_create(Subject, **fields) for fields in subjects_final]
