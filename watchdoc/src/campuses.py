from enum import Enum


class Campus(Enum):
    MOSCOW = "MO"
    SAINT_PETERSBURG = "SP"
    NIZHNY_NOVGOROD = "NN"
    PERM = "PE"

    @property
    def label(self) -> str:
        if self == Campus.MOSCOW:
            return "Москва"
        if self == Campus.SAINT_PETERSBURG:
            return "Санкт-Петербург"
        if self == Campus.NIZHNY_NOVGOROD:
            return "Нижний Новгород"
        if self == Campus.PERM:
            return "Пермь"
        raise ValueError("Unknown campus")

    @staticmethod
    def choices():
        campuses = [
            Campus.MOSCOW,
            Campus.SAINT_PETERSBURG,
            Campus.NIZHNY_NOVGOROD,
            Campus.PERM,
        ]
        return [(c.value, c.label) for c in campuses]

    @staticmethod
    def values():
        return [c[0] for c in Campus.choices()]

    @staticmethod
    def labels():
        return [c[1] for c in Campus.choices()]
