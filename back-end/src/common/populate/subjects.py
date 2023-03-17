from common.models.subjects import Subject
from common.models.milspecialties import Milspecialty
from common.models.universities import Campus

from common.utils.populate import get_or_create


def create_subjects(milspecialties: Milspecialty) -> list[Subject]:
    milspecialties_codes = ['453000', '453100', '461300', '094001']
    milspecialties = {code: milspecialties[code] for code in milspecialties_codes}
    subjects = [
        {
            "title": "Тактическая подготовка",
            "annotation": "Педагогический процесс, направленный на овладение рациональными формами ведения спортивной борьбы в процессе специфической соревновательной деятельности."
        },
        {
            "title": "Военная топография",
            "annotation": "Дисциплина военного дела, изучающая методы и средства оценки местности, ориентирования на местности и осуществления полевых измерений для обеспечения боевой деятельности войск (сил), определяющая правила по ведению рабочих карт командиров и разработки графических боевых документов."
        },
        {
            "title": "Строевая подготовка",
            "annotation": "Предмет обучения военнослужащих и подразделений умению выполнять команды, строевые приёмы с оружием и без оружия."
        }
    ]
    subjects_final = []
    for subject in subjects:
        for milspecialty in milspecialties:
            subjects_final.append(subject.copy())
            subjects_final[-1].update({"milspecialty": milspecialties[milspecialty]})

    return [get_or_create(Subject, **fields) for fields in subjects_final]
