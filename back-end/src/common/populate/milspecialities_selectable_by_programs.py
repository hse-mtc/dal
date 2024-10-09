from common.models.milspecialties import Milspecialty

from common.models.universities import (
    Program,
)

def create_milspecialities_selectable_by_programs(milspecialties: dict[str, Milspecialty], programs: dict[str, Milspecialty]):
    milspecialties["453000"].selectable_by.add(
        programs["Информационная безопасность"],
        programs["Информатика и вычислительная техника"],
        programs["Программная инженерия"],
    )
    milspecialties["453100"].selectable_by.add(
        programs["Информационная безопасность"],
        programs["Информатика и вычислительная техника"],
        programs["Программная инженерия"],
    )
