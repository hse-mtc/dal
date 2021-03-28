from enum import Enum


class RelativeType(Enum):
    FATHER = "FA"
    MOTHER = "MO"
    BROTHER = "BR"
    SISTER = "SI"

    @property
    def label(self) -> str:
        if self == RelativeType.FATHER:
            return "отец"
        if self == RelativeType.MOTHER:
            return "мать"
        if self == RelativeType.BROTHER:
            return "брат"
        if self == RelativeType.SISTER:
            return "сестра"
        raise ValueError("Unknown type of relative")

    @staticmethod
    def choices():
        types = [
            RelativeType.FATHER,
            RelativeType.MOTHER,
            RelativeType.BROTHER,
            RelativeType.SISTER,
        ]
        return [(t.value, t.label) for t in types]

    @staticmethod
    def values():
        return [t[0] for t in RelativeType.choices()]

    @staticmethod
    def labels():
        return [t[1] for t in RelativeType.choices()]
