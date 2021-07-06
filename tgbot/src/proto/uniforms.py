from enum import Enum
from dataclasses import dataclass


class Headdress(Enum):
    CAP = "CA"
    HAT = "HA"

    def __str__(self) -> str:
        to_string: dict[Headdress, str] = {
            Headdress.CAP: "кепка",
            Headdress.HAT: "шапка",
        }
        return to_string[self]


class Outerwear(Enum):
    PEA_COAT = "PC"
    JACKET = "JA"

    def __str__(self) -> str:
        to_string: dict[Outerwear, str] = {
            Outerwear.PEA_COAT: "бушлат",
            Outerwear.JACKET: "китель",
        }
        return to_string[self]


@dataclass
class Uniform:
    headdress: Headdress
    outerwear: Outerwear
    milfaculty: str

    @staticmethod
    def from_raw(body) -> "Uniform":
        return Uniform(
            headdress=Headdress(body["headdress"]),
            outerwear=Outerwear(body["outerwear"]),
            milfaculty=body["milfaculty"],
        )

    def __str__(self) -> str:
        return (
            f"Головной убор: {self.headdress}.\n"
            f"Нательная одежда: {self.outerwear}.\n"
        )
