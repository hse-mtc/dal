from common.utils.populate import get_or_create

from lms.models.common import Milfaculty
from lms.models.uniforms import Uniform


def create_uniforms(milfaculties: dict[str, Milfaculty]):
    for milfaculty in milfaculties:
        fields = {
            "headdress": "CA",
            "outerwear": "JA",
            "milfaculty": milfaculties[milfaculty],
        }
        get_or_create(Uniform, **fields)
